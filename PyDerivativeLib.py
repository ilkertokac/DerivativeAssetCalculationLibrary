import math
from scipy.stats import norm
import matplotlib.pyplot as plt
from enum import Enum
import pandas as pd
from statsmodels.api import OLS,add_constant

class AssetType(Enum):
    C = 1
    P = 2

class DerivativeType(Enum):
    Warrant = 1
    Option = 2

class Graph_Case(Enum):
    Price = 1
    Delta = 2
    Theta = 3
    Vega = 4
    Rho = 5
    Gamma = 6

class Future_Type(Enum):
    Stock = 1
    Index = 2
    Currency = 3
    Metal = 4
    Interest = 5

class OptionCalculate:
    def __init__(
        self,
        Type,
        UnderlyingPrice,
        StrikePrice,
        DaysToMaturity,
        DomesticRate,
        ImpliedVolatility,
        Dividend,
    ):
        self.__Type = str(Type)
        self._UnderlyingPrice = UnderlyingPrice
        self._StrikePrice = StrikePrice
        self._DaysToMaturity = DaysToMaturity
        self._DomesticRate = DomesticRate
        self._ImpliedVolatility = ImpliedVolatility
        self._Dividend = Dividend
        self.__DaysToMaturity = DaysToMaturity / 365
        self.__DomesticRate = DomesticRate / 100
        self.__ImpliedVolatility = ImpliedVolatility / 100
        self.__Dividend = Dividend / 100
        self.__d_one = None
        self.__d_two = None
        self.__NdOne = None
        self.__NdTwo = None
    
    @property
    def dOne(self):
        if not self.__d_one:
            returns = math.log(
                (self._UnderlyingPrice / self._StrikePrice)
                + (
                    self.__DomesticRate
                    - self.__Dividend
                    + 0.5 * self.__ImpliedVolatility**2
                )
                * self.__DaysToMaturity
            ) / (self.__ImpliedVolatility * math.sqrt(self.__DaysToMaturity))
            self.__d_one = returns
        return self.__d_one

    @property
    def NdOne(self):
        if not self.__NdOne:
            returns = math.exp(-(self.dOne**2) / 2) / (math.sqrt(2 * math.pi))
            self.__NdOne = returns
        return self.__NdOne

    @property
    def dTwo(self):
        if not self.__d_two:
            returns = self.dOne - self.__ImpliedVolatility * math.sqrt(
                self.__DaysToMaturity
            )
            self.__d_two = returns
        return self.__d_two

    @property
    def NdTwo(self):
        if not self.__NdTwo:
            returns = norm.cdf(self.dTwo)
            self.__NdTwo = returns
        return self.__NdTwo

    def Price(self):
        """

            Fonksiyon, gerekli parametreler girdiğinde opsiyonun Black-Scholes yöntemine göre teorik fiyatını hesaplar

        """
        CallPrice = math.exp(
            -self.__Dividend * self.__DaysToMaturity
        ) * self._UnderlyingPrice * norm.cdf(
            self.dOne
        ) - self._StrikePrice * math.exp(
            -self.__DomesticRate * self.__DaysToMaturity
        ) * norm.cdf(
            self.dOne - self.__ImpliedVolatility * math.sqrt(self.__DaysToMaturity)
        )
        PutPrice = self._StrikePrice * math.exp(
            -self.__DomesticRate * self.__DaysToMaturity
        ) * norm.cdf(-self.dTwo) - math.exp(
            -self.__Dividend * self.__DaysToMaturity
        ) * self._UnderlyingPrice * norm.cdf(
            -self.dOne
        )
        if self.__Type == "C":
            returns = CallPrice
        elif self.__Type == "P":
            returns = PutPrice
        else:
            returns = "C or P can be entered as option type."
        return returns

    def Delta(self):
        """

            Fonksiyon, gerekli parametreler girdiğinde opsiyonun delta greeksini hesaplar

        """
        CallDelta = norm.cdf(self.dOne)
        PutDelta = CallDelta - 1
        if self.__Type == "C":
            returns = CallDelta
        elif self.__Type == "P":
            returns = PutDelta
        else:
            returns = "C or P can be entered as option type."
        return returns

    def Theta(self):
        """

            Fonksiyon, gerekli parametreler girdiğinde opsiyonun theta greeksini hesaplar

        """
        CT = (
            -(self._UnderlyingPrice * self.__ImpliedVolatility * self.NdOne)
            / (2 * math.sqrt(self.__DaysToMaturity))
            - self.__DomesticRate
            * self._StrikePrice
            * math.exp(-self.__DomesticRate * self.__DaysToMaturity)
            * self.NdTwo
        )
        CallTheta = CT / 365
        PT = -(self._UnderlyingPrice * self.__ImpliedVolatility * self.NdOne) / (
            2 * math.sqrt(self.__DaysToMaturity)
        ) + self.__DomesticRate * self._StrikePrice * math.exp(
            -self.__DomesticRate * self.__DaysToMaturity
        ) * (
            1 - self.NdTwo
        )
        PutTheta = PT / 365
        if self.__Type == "C":
            returns = CallTheta
        elif self.__Type == "P":
            returns = PutTheta
        else:
            returns = "C or P can be entered as option type."
        return returns

    def PercentTheta(self):
        """

            Fonksiyon, gerekli parametreler girdiğinde opsiyonun yüzde theta greeksini hesaplar. 
            Theta değişimişiniş fiyatı yüzde kaç değiştirir onu gösterir.

        """
        returns = 100 * (((self.Price() + self.Theta()) / self.Price()) - 1)
        return returns

    def Vega(self):

        """

            Fonksiyon, gerekli parametreler girdiğinde opsiyonun vega greeksini hesaplar. 


        """
        returns = (
            0.01
            * self._UnderlyingPrice
            * math.sqrt(self.__DaysToMaturity)
            * self.NdOne
        )
        return returns

    def Gamma(self):

        """

            Fonksiyon, gerekli parametreler girdiğinde opsiyonun gamma greeksini hesaplar. 


        """
        returns = self.NdOne / (
            self._UnderlyingPrice
            * (self.__ImpliedVolatility * math.sqrt(self.__DaysToMaturity))
        )
        return returns

    def Rho(self):

        """

            Fonksiyon, gerekli parametreler girdiğinde opsiyonun rho greeksini hesaplar. 


        """
        CallRho = (
            0.01
            * self._StrikePrice
            * self.__DaysToMaturity
            * math.exp(-self.__DomesticRate * self.__DaysToMaturity)
            * norm.cdf(self.dTwo)
        )
        PutRho = (
            -0.01
            * self._StrikePrice
            * self.__DaysToMaturity
            * math.exp(-self.__DomesticRate * self.__DaysToMaturity)
            * (1 - norm.cdf(self.dTwo))
        )
        if self.__Type == "C":
            returns = CallRho
        elif self.__Type == "P":
            returns = PutRho
        else:
            returns = "C or P can be entered as option type."
        return returns

    def Sensitivity(self):
        returns = 1 / self.Delta() / 100
        return returns

    def Flexibility(self):
        returns = self._UnderlyingPrice / self.Price()
        return returns

    def BasicValue(self):
        callValue = self._UnderlyingPrice - self._StrikePrice
        putValue = self._StrikePrice - self._UnderlyingPrice
        if self.__Type == "C":
            returns = callValue
        else:
            returns = putValue
        return returns

    def TimeValue(self):
        returns = self.Price() - self.BasicValue()
        return returns

    def CostDifference(self):
        callValue = self.Price() + self._StrikePrice - self._UnderlyingPrice
        putValue = self.Price() + self._UnderlyingPrice - self._StrikePrice
        if self.__Type == "C":
            returns = callValue
        else:
            returns = putValue
        return returns

    def PercentCostDifference(self):
        returns = self.CostDifference() / self._UnderlyingPrice * 100
        return returns

    def Leverage(self):
        returns = round(abs(self._UnderlyingPrice / self.Price() * self.Delta()), 0)
        return returns

class WarrantCalculate(OptionCalculate):
    def __init__(
        self,
        Type,
        UnderlyingPrice,
        StrikePrice,
        DaysToMaturity,
        DomesticRate,
        ImpliedVolatility,
        Dividend,
        ConversionRate=1,
    ):
        super().__init__(
            Type,
            UnderlyingPrice,
            StrikePrice,
            DaysToMaturity,
            DomesticRate,
            ImpliedVolatility,
            Dividend,
        )
        self.__Type = str(Type)
        self._UnderlyingPrice = UnderlyingPrice
        self._StrikePrice = StrikePrice
        self.__DaysToMaturity = DaysToMaturity / 365
        self.__DomesticRate = DomesticRate / 100
        self.__ImpliedVolatility = ImpliedVolatility / 100
        self.__Dividend = Dividend / 100
        self.__ConversionRate = ConversionRate

    def Price(self):
        returns = super().Price() * self.__ConversionRate
        return returns

    def Delta(self):
        return super().Delta()

    def Theta(self):
        return super().Theta() * self.__ConversionRate

    def Vega(self):
        return super().Vega() * self.__ConversionRate

    def Rho(self):
        return super().Rho() * self.__ConversionRate

    def Gamma(self):
        return super().Gamma()

    def BasicLeverage(self):
        returns = self._UnderlyingPrice / self.Price() * self.__ConversionRate
        return returns

    def Leverage(self):
        returns = round(abs(self.BasicLeverage() * self.Delta()), 0)
        return returns

    def Sensitivity(self):
        returns = (1 / (self.Delta() * self.__ConversionRate)) / 100
        return returns

    def Flexibility(self):
        return super().Flexibility() * self.__ConversionRate

    def BasicValue(self):
        return super().BasicValue() * self.__ConversionRate

    def TimeValue(self):
        return super().TimeValue()

    def CostDifference(self):
        callValue = (
            (self.Price() / self.__ConversionRate)
            + self._StrikePrice
            - self._UnderlyingPrice
        )
        putValue = (
            (self.Price() / self.__ConversionRate)
            + self._UnderlyingPrice
            - self._StrikePrice
        )
        if self.__Type == "C":
            returns = callValue
        else:
            returns = putValue
        return returns

    def PercentCostDifference(self):
        returns = self.CostDifference() / self._UnderlyingPrice * 100
        return returns

class Future:
    def __init__(
        self,
        Type,
        UnderlyingPrice,
        DaysToMaturity,
        DomesticRate,
        ForeignRate,
        Dividend,
    ):
        self.__Type = Type
        self._UnderlyingPrice = UnderlyingPrice
        self.__DaysToMaturity = DaysToMaturity / 365
        self.__DomesticRate = DomesticRate / 100
        self.__ForeignRate = ForeignRate / 100
        self.__Dividend = Dividend / 100
    
    def TheoreticalPrice(self, AnnualStorageCostRate=0, GoldLeaseRate=0, PresentValue=1):
        if self.__Type == Future_Type.Index or self.__Type == Future_Type.Stock:
            prices = self._UnderlyingPrice * math.exp((self.__DomesticRate - self.__Dividend) * self.__DaysToMaturity)
        elif self.__Type == Future_Type.Currency:
            prices = self._UnderlyingPrice * math.exp((self.__DomesticRate - self.__ForeignRate) * self.__DaysToMaturity)
        elif self.__Type == Future_Type.Metal:
            prices = self._UnderlyingPrice * math.exp((self.__DomesticRate + (AnnualStorageCostRate / 100) - (GoldLeaseRate / 100)) * self.__DaysToMaturity)
        elif self.__Type == Future_Type.Interest:
            prices = (self._UnderlyingPrice - PresentValue) * math.exp(self.__DomesticRate * self.__DaysToMaturity)
        else:
            print(Exception)
        return prices
    
    def HedgeRatio(self,MarketPrice,FuturePrice): #TODO None geliyor
        if MarketPrice is None or FuturePrice is None:
            rko = ("-----------------")
        elif len(MarketPrice) != len(FuturePrice):
            rko = ("-----------------")
        elif len(MarketPrice) == len(FuturePrice):
            MarketReturn = pd.DataFrame(MarketPrice).pct_change().dropna(how="all")
            FutureReturn = pd.DataFrame(FuturePrice).pct_change().dropna(how="all")
            X = add_constant(MarketReturn)
            y = FutureReturn
            model = OLS(y,X).fit()
            rko = model.params.values[1]
        return rko

class Graphs:
    def __init__(
        self,
        Type,
        Asset_Type: AssetType,
        UnderlyingPrice,
        StrikePrice,
        DaysToMaturity,
        DomesticRate,
        ImpliedVolatility,
        Dividend,
        ConversionRate = 1
    ):
        self.__Type = str(Type)
        self.__assetType = Asset_Type
        self._UnderlyingPrice = UnderlyingPrice
        self._StrikePrice = StrikePrice
        self.__DaysToMaturity = DaysToMaturity
        self.__DomesticRate = int(DomesticRate)
        self.__ImpliedVolatility = ImpliedVolatility
        self.__Dividend = Dividend
        self.__ConversionRate = ConversionRate
    
        if any(
            val < 0
            for val in [
                self._UnderlyingPrice,
                self._StrikePrice,
                self.__DaysToMaturity,
                self.__DomesticRate,
                self.__ImpliedVolatility,
                self.__Dividend,
                self.__ConversionRate,
            ]
        ):
            raise ValueError("Values cannot be negative. Check the entered values.")
        
    def DerivativeToolSimulationGraph(self,GraphCase: Graph_Case = Graph_Case.Price,percentage_change=0.05):
        price_range = [self._UnderlyingPrice * (1 + percentage_change) ** n for n in range(-5, 5 + 1)]
        asset_value = []
        match self.__Type:
            case "Option" | "Opsiyon":
                match GraphCase:
                    case Graph_Case.Price:
                        for price in price_range:
                            option = OptionCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend)
                            asset_value.append(option.Price())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Price():.6f}")
                    case Graph_Case.Delta:
                        for price in price_range:
                            option = OptionCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend)
                            asset_value.append(option.Delta())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Delta():.6f}")
                    case Graph_Case.Theta:
                        for price in price_range:
                            option = OptionCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend)
                            asset_value.append(option.Theta())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Theta():.6f}")
                    case Graph_Case.Gamma:
                        for price in price_range:
                            option = OptionCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend)
                            asset_value.append(option.Gamma())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Gamma():.6f}")
                    case Graph_Case.Vega:
                        for price in price_range:
                            option = OptionCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend)
                            asset_value.append(option.Vega())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Vega():.6f}")
                    case Graph_Case.Rho:
                        for price in price_range:
                            option = OptionCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend)
                            asset_value.append(option.Rho())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Rho():.6f}")
                    case _:
                        raise TypeError("Girilen grafik tipi parametresi doğru değildir.")
                    
            case "Warrant" | "warrant":
                match GraphCase:
                    case Graph_Case.Price:
                        for price in price_range:
                            option = WarrantCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend,self.__ConversionRate)
                            asset_value.append(option.Price())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Price():.6f}")
                    case Graph_Case.Delta:
                        for price in price_range:
                            option = WarrantCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend,self.__ConversionRate)
                            asset_value.append(option.Delta())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Delta():.6f}")
                    case Graph_Case.Theta:
                        for price in price_range:
                            option = WarrantCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend,self.__ConversionRate)
                            asset_value.append(option.Theta())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Theta():.6f}")
                    case Graph_Case.Gamma:
                        for price in price_range:
                            option = WarrantCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend,self.__ConversionRate)
                            asset_value.append(option.Gamma())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Gamma():.6f}")
                    case Graph_Case.Vega:
                        for price in price_range:
                            option = WarrantCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend,self.__ConversionRate)
                            asset_value.append(option.Vega())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Vega():.6f}")
                    case Graph_Case.Rho:
                        for price in price_range:
                            option = WarrantCalculate(self.__assetType,price,self._StrikePrice,self.__DaysToMaturity,self.__DomesticRate,self.__ImpliedVolatility,self.__Dividend,self.__ConversionRate)
                            asset_value.append(option.Rho())
                            print(f"Underlying Price: {price:.2f} Warrant Price: {option.Rho():.6f}")
                    case _:
                        raise TypeError("Girilen grafik tipi parametresi doğru değildir.")
            case _:
                raise TypeError("Girilen tip parametresi doğru değildir.")
        plt.plot(price_range, asset_value, marker="o")
        plt.xlabel("Underlying Price")
        plt.ylabel(f"Warrant {Graph_Case(GraphCase).name}")
        plt.title(
            f"The Relationship Option {Graph_Case(GraphCase).name} and Underlying Price"
        )
        plt.grid()
        plt.show()


"""

Örnek kullanım(Opiyon Fiyat ve Greeksleri)
opsiyon = OptionCalculate("P",10,10,10,10,50,0)
print(opsiyon.Price())

"""




# Grafik için örnek kullanım
opsiyon = Graphs("Option","C",10,10,10,10,50,0)
opsiyon.DerivativeToolSimulationGraph(Graph_Case.Delta,percentage_change=0.05)




    