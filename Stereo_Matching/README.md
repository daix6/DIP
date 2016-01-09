## DIP Final Project : Stereo Matching

### Details

1. Find codes in src/
2. Find report in doc/report.pdf
3. Find results in dest/
4. bin/ contains the quality details for all cases and a script that transform the result to LaTex tabular form...

I have run with 33x33 support window in ASW **only for the former 6th testcases**, and I denote at filename with '_33'. And all of other results were run with 5x5 support window.

### How to Run

1. CLI (Better)

```bash
  mkdir bin                                       # For .class file

  # Note: If you are under Windows, please replace ':' with ';'.

  javac -cp .:libs/* -sourcepath src -d bin src/* # Compile
  java -cp .:libs/*:bin Test -case casename       # Run single case, casename is case sensitive.
  java -cp .:libs/*:bin Test -all                 # Run all case
```

If you are under windows, you can simple run the `run.sh` file under the root directory, which run case *Aloe* only.

2. Eclipse

If you have eclipse for java, you can try use it simply. And do not forget to add arguments!

### PS

Thank you for this term's hard working~! ( =

戴旋 13331043
