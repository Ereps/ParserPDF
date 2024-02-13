file = "Corpus_result/torres-moreno.txt"

with open(file, 'r', encoding="utf-8") as txtFile :
    lines = txtFile.readlines()
    count = 0
    for line in lines :
        count += 1

        line = line.replace("´e", "é")
        line = line.replace("`e", "è")
        line = line.replace("`a", "à")

        print("Line{}: {}".format(count, line.strip()))

        if (count == 20) : break