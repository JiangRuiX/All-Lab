name=input('Enter your name: (use "stop" to finish)')
end='stop'
count=0
while name!=end:
    count+=1
    name=input('Enter your name: ')
if count>0:
    print('Number of names entered',count)
else:
    print('No names were entered.')