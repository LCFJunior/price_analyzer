from utils.money import Money


print(Money.parse("R$\n5.042"))

print(Money.parse("R$ 5.042,90"))

print(Money.parse("R$499"))

print(Money.parse(None))