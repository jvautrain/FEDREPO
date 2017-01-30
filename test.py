jim='Autauga County, AL (01001)'
start=jim.find("(")
print(start.__str__())
joe=jim[start+1:start+6]
print(joe)