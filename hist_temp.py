path = "/home/pi/Temperature/log/templog.txt"
f = open(path, 'r')
package = f.readline()
print(package)
