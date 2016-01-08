import java.awt.Color;
import java.awt.image.BufferedImage;

import org.apache.commons.cli.CommandLine;

public class Test {
  public static void runAllCases() {
    String[] cases = Utils.getAllCases();

    for (String testcase : cases) {
      BufferedImage left = Utils.getImage(testcase, Utils.LEFT),
                    right = Utils.getImage(testcase, Utils.RIGHT),
                    benchmark_left = Utils.getImage(testcase, Utils.BENCHMARK_LEFT),
                    benchmark_right = Utils.getImage(testcase, Utils.BENCHMARK_RIGHT);

      // SSD
      StereoMatching sm = new StereoMatching(left, right);
      sm.caculateDisparity(new SSD());;
      sm.evaluate(benchmark_left, benchmark_right);
      sm.printBad(testcase, "SSD");
      Utils.saveImage(new BufferedImage[]{sm.disp_l, sm.disp_r}, testcase, "SSD");

      // NCC
      sm.caculateDisparity(new NCC());
      sm.evaluate(benchmark_left, benchmark_right);
      sm.printBad(testcase, "NCC");
      Utils.saveImage(new BufferedImage[]{sm.disp_l, sm.disp_r}, testcase, "NCC");

      // ASW
      sm.caculateDisparityCIELab(new ASW());
      sm.evaluate(benchmark_left, benchmark_right);
      sm.printBad(testcase, "ASW");
      Utils.saveImage(new BufferedImage[]{sm.disp_l, sm.disp_r}, testcase, "ASW");

      // Add 10 intensity to right-eye image
      StereoMatching sm10 = new StereoMatching(left, Utils.addIntensity(right, 10));
      // SSD
      sm10.caculateDisparity(new SSD());
      sm10.evaluate(benchmark_left, benchmark_right);
      sm10.printBad(testcase, "SSD");
      Utils.saveImage(new BufferedImage[]{sm10.disp_l, sm10.disp_r}, testcase, "SSD_ADD_10");

      // NCC
      sm10.caculateDisparity(new NCC());
      sm10.evaluate(benchmark_left, benchmark_right);
      sm10.printBad(testcase, "NCC");
      Utils.saveImage(new BufferedImage[]{sm10.disp_l, sm10.disp_r}, testcase, "NCC_ADD_10");
    }
  }

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

        // SSD
        sm.caculateDisparity(new SSD());
        sm.evaluate(benchmark_left, benchmark_right);
        sm.printBad(testcase, "SSD");
        Utils.saveImage(new BufferedImage[]{sm.disp_l, sm.disp_r}, testcase, "SSD");

        // NCC
        sm.caculateDisparity(new NCC());
        sm.evaluate(benchmark_left, benchmark_right);
        sm.printBad(testcase, "NCC");
        Utils.saveImage(new BufferedImage[]{sm.disp_l, sm.disp_r}, testcase, "NCC");

        // ASW
        sm.caculateDisparityCIELab(new ASW());
        sm.evaluate(benchmark_left, benchmark_right);
        sm.printBad(testcase, "ASW");
        Utils.saveImage(new BufferedImage[]{sm.disp_l, sm.disp_r}, testcase, "ASW");

        // Add 10 intensity to right-eye image
        StereoMatching sm10 = new StereoMatching(left, Utils.addIntensity(right, 10));

        // SSD
        sm10.caculateDisparity(new SSD());
        sm10.evaluate(benchmark_left, benchmark_right);
        sm10.printBad(testcase, "SSD");
        Utils.saveImage(new BufferedImage[]{sm10.disp_l, sm10.disp_r}, testcase, "SSD_ADD_10");

        // NCC
        sm10.caculateDisparity(new NCC());
        sm10.evaluate(benchmark_left, benchmark_right);
        sm10.printBad(testcase, "NCC");
        Utils.saveImage(new BufferedImage[]{sm10.disp_l, sm10.disp_r}, testcase, "NCC_ADD_10");

    } else if (cmd.hasOption("all")) {
        runAllCases();
    }
  }
}
