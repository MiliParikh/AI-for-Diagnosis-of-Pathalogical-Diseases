s = open("htmlgen.html")
i = 2
disease = []
for lines in s:
    if '<option value' in lines:
        try:
            x = lines.split('"')
            print(x[1])
            disease.append(x[1])
            i+=1

            if i > 50:
                break
       
        except:
            pass
