class Bundles(object):

    def __init__(self, bundles):
        try:
            iter(bundles)
        except TypeError:
            raise TypeError("bundles must be an iterable")
        self.bundles = bundles

    def __str__(self):
        return ','.join(self.bundles)

    def __unicode__(self):
        return u', '.join(self.bundles)
