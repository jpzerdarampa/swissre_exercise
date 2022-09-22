# swissre_exercise

Example of script executions:

- Most frequent IP:       Python Analyzer.py -i "access.log" -o "output.json" -m
- Least frequent IP:      Python Analyzer.py -i "access.log" -o "output.json" -l
- Events per second:      Python Analyzer.py -i "access.log" -o "output.json" -e
- Total amount of Bytes:  Python Analyzer.py -i "access.log" -o "output.json" -t


Example how to run the script in a container of Docker:

- Build the dockerfile:
    sudo docker image build -t python:0.0.1 .
- Copy the input file (logs) into the container:
    docker cp access.log container:/workdir
- Run the container with parameters:
    sudo docker run python:0.0.1 -i "access.log" -o "output.json" -m
