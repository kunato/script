class CollinsSpan:

    def __init__(self, i, j, h, score):
        self.i = i
        self.j = j
        self.h = h
        self.score = score

    def __str__(self):
        return "[%s, %s, %s, %s]" % (self.i, self.j, self.h, self.score)

class EisnerSpan:

    def __init__(self, i, j, t, score):
        self.i = i
        self.j = j
        self.t = t
        self.score = score

    def __str__(self):
        return "[%s, %s, %s, %s]" % (self.i, self.j, self.t, self.score)

class EisnerParser:

    def __init__(self):
        self.chart = None

    def parse(self, words):
        self.init_spans(words)

        # merge spans in a bottom-up manner
        for l in xrange(0, len(words)):
            for i in xrange(0, len(words)):
                j = i + l
                if j >= len(words): break

                # rule1 and 2
                for k in xrange(i, j):
                    span_l = self.chart[i][k][0]
                    span_r = self.chart[k+1][j][1]
                    # apply rule1
                    score = self.get_score(words, span_l, span_r)
                    span = EisnerSpan(i, j, 2, score)
                    self.add_span(span)
                    # apply rule2
                    score = self.get_score(words, span_r, span_l)
                    span = EisnerSpan(i, j, 3, score)
                    self.add_span(span)

                # rule3
                for k in xrange(i+1, j+1):
                    span_l = self.chart[i][k][2]
                    span_r = self.chart[k][j][0]
                    score = span_l.score + span_r.score
                    span = EisnerSpan(i, j, 0, score)
                    self.add_span(span)

                # rule4
                for k in xrange(i, j):
                    span_l = self.chart[i][k][1]
                    span_r = self.chart[k][j][3]
                    score = span_l.score + span_r.score
                    span = EisnerSpan(i, j, 1, score)
                    self.add_span(span)
                    
        best = self.find_best(0, len(words)-1)
        return best

    def init_spans(self, words):
        # initialize chart as 3-dimensional list
        length = len(words)
        chart = []
        for i in xrange(length):
            chart.append([])
            for j in xrange(length):
                chart[i].append([None] * 4)
        self.chart = chart

        # add left and right spans to the chart
        for i in xrange(0, len(words)):
            span = EisnerSpan(i, i, 0, 0.0)
            self.add_span(span)
            span = EisnerSpan(i, i, 1, 0.0)
            self.add_span(span)

    def add_span(self, new_span):
        i, j, t = new_span.i, new_span.j, new_span.t
        old_span = self.chart[i][j][t]
        if old_span is None or old_span.score < new_span.score:
            self.chart[i][j][t] = new_span # update chart

    def get_score(self, words, head, dep):
        if head.t == 0 or head.t == 2:
            h = head.i
        elif head.t == 1 or head.t == 3:
            h = head.j
        h_word = words[h]
        if h_word == "read":
            score = 1.0
        elif h_word == "novel":
            score = 0.3
        else:
            score = 0.1
        # calculate score based on arc-factored model
        return head.score + dep.score + score

    """ Find the highest-scored span """
    def find_best(self, i, j):
        num_words = len(self.chart)
        best_span = None
        # for x in range(0,len(self.chart)):
        #     for y in range(len(self.chart)):
        #         for t in range(4):
        #             print ((x,y),str(self.chart[x][y][t]))
        collins = []
        for t in xrange(num_words):
            best = 0
            best_index = -1
            first = self.chart[0][t][1]
            second = self.chart[t][num_words-1][0]
            collins.append(CollinsSpan(0,num_words-1,t,first.score+second.score))

        best_collin = -1
        best_collin_index = -1
        for x in range(0,len(collins)):
            # print ("sc",str(collins[x]))
            if(collins[x].score > best_collin):
                best_collin = collins[x].score
                best_collin_index = x
        return collins[best_collin_index]

# run
p = EisnerParser()
span = p.parse(["She", "read", "a", "short", "novel"])
print span