__author__ = 'wendy'


class Utils:

    @staticmethod
    def ranklist(l):
        ''' given l=[a, b, c, c, c, b]
        return counts and ordered list of tuples
        result = [(c, 3), (b, 2), (a, 1)]
        '''
        result = []
        for entry in set(l):
            result.append((entry, l.count(entry)))
        result.sort(key = lambda x: -x[1])
        return result