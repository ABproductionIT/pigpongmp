file = open("temp.txt", "r")
lista = []
a = file.read()
b = list(map(float, a.split(", ")))
print(b)
# type of self.pos is <class 'kivy.properties.ObservableReferenceList'>
file.close()