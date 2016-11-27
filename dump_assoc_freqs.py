"""
You can run this locally simulating some map-reduce in a cluster, e.g.:
$ python dump_assoc_freqs.py -r local --verbose
       --jobconf mapreduce.job.maps=10
             go_assoc_2006-11-01_association.txt
             go_assoc_2006-11-01_evidence.txt
"""

from mrjob.job import MRJob, MRStep

class MRGOAFrecCounter(MRJob):
     """Map-reduces the MySQL dump files of the GOA database.
     Gets frequencies of each term and frequencies of evidence codes
     per term.
     """
     SORT_VALUES = True

     def steps(self):
        """The first step joins the evidence with the associations.
        The second counts the frequencies.
        """
        return [
            MRStep(mapper=self.mapper_join,
                   reducer=self.reducer_join),
            MRStep(mapper=self.mapper_count_freq,
                   reducer=self.reducer_count_freq)
        ]


     def mapper_join(self, _, line):
         """Receive both associations and evidence lines.
         Maps to the association id plus additional info.
         """
         splits = line.split("\t")
         if len(splits)==7:
             assoc_id = splits[0]
             go_term = splits[1]
             is_not = splits[3]
             date = splits[5]
             database = splits[6]
             yield assoc_id, [go_term, is_not, date, database]
         else:
             assoc_id = splits[2]
             evidence = splits[1]
             yield assoc_id, [evidence]


     def reducer_join(self, key, values):
         """Produces a line per annotation-evidence.
         """
         values = [x for x in values]
         # if there were no evidence codes for a assoc_id, there is
         # only a value, which it itself a list.
         if len(values) > 1: # our join hit

            # Separate the elements from associations table:
            # Generate a line for each evidence code.
            for v in values[1:]:
                temp =values[0][:] # Copy the list.
                temp.append(v[0])  # Append the evidence code.
                yield key, temp
         else: # our join missed, maybe evidence code missing?
            values[0].append("NA")
            yield key, values[0]


     def mapper_count_freq(self, _, data):
         """Takes as input something as:
         associd [go_term, is_none, date, db_id, evidence_code]
         """
         go_term = data[0]
         yield go_term, data[1:]


     def reducer_count_freq(self, key, values):
         """Count the frequencies (total and per evidence code) for
            each GO term.
         """
         values = [v for v in values]
         # Count frequencies of evidence codes.
         counts = {}
         counts["TOTAL"] = 0
         for v in values:
             code = v[3]
             if code in counts:
                 counts[code] = counts[code] +1
             else:
                 counts[code]=1
             counts["TOTAL"] += 1
         # The value is encoded by default as JSON.
         # An example:
         #
         yield None, (key, counts)



if __name__ == "__main__":
    MRGOAFrecCounter.run()
