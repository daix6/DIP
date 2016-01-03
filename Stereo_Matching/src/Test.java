import java.awt.image.BufferedImage;

import org.apache.commons.cli.CommandLine;

public class Test {
  public static void runAllCases() {}

  public static void main(String[] args) {
    // TODO Auto-generated method stub
    CommandLine cmd = Utils.parser(args);

    if (cmd.hasOption("case")) {
        String testcase = cmd.getOptionValue("case");
        BufferedImage left = Utils.getImage(testcase, Utils.LEFT),
                right = Utils.getImage(testcase, Utils.RIGHT),
                benchmark_left = Utils.getImage(testcase, Utils.BENCHMARK_LEFT),
                benchmark_right = Utils.getImage(testcase, Utils.BENCHMARK_RIGHT);
        StereoMatching sm = new StereoMatching(left, right);
        sm.ssd();
        sm.evaluate(benchmark_left, benchmark_right);
        sm.printBad(testcase);
        Utils.saveImage(new BufferedImage[]{sm.disp_l, sm.disp_r}, testcase, "SSD");
    } else if (cmd.hasOption("all")) {
        runAllCases();
    }
  }
}
