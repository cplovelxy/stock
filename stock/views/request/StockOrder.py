class stock_order(object):
    def __init__(self, **kwargs):
        self.stockCode = kwargs.get('stockCode')
        self.stockName = kwargs.get('stockName')
        self.entrustAmount = kwargs.get('entrustAmount')
        self.entrustPrice = kwargs.get('entrustPrice')
        self.entrustProp = kwargs.get('entrustProp')
        self.entrustType = kwargs.get('entrustType')
        self.exchangeType = kwargs.get('exchangeType')
        self.forceEntrustFlag = kwargs.get('forceEntrustFlag')

