# For Windows

mkdir bin

javac -cp .\;libs/* -sourcepath src -d bin src/*
java -cp .\;libs/*\;bin Test -case Aloe
# java -cp .\;libs/*;bin Test -all

# For Linux

# mkdir bin

# javac -cp .:libs/* -sourcepath src -d bin src/*
# java -cp .:libs/*:bin Test -case Aloe
# java -cp .:libs/*:bin Test -all