import java.awt.image.BufferedImage;
import java.awt.image.DataBufferByte;
import java.awt.image.WritableRaster;
import java.io.File;

import javax.imageio.ImageIO;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

public class Utils {
  static public final int LEFT = 0;
  static public final int RIGHT = 1;
  static public final int BENCHMARK_LEFT = 2;
  static public final int BENCHMARK_RIGHT = 3;
  static public final String LEFT_IMAGE = "view1.png";
  static public final String RIGHT_IMAGE = "view5.png";
  static public final String LEFT_BENCHMARK = "disp1.png";
  static public final String RIGHT_BENCHMARK = "disp5.png";
  
  public static CommandLine parser(String[] args) {
    Options opts = new Options();
    opts.addOption("case", true, "The testcase that you want to run with");
    opts.addOption("all", false, "Run all testcase or not.");
    
    CommandLineParser parser = new DefaultParser();
    CommandLine cmd = null;
    try {
      cmd = parser.parse(opts, args);
    } catch( ParseException exp ) {
      // oops, something went wrong
      System.err.println( "Parsing failed.  Reason: " + exp.getMessage() );
    }

    return cmd;
  }

  public static String getAssetsDir() {
    File file = new File("");
    String parentDir = file.getAbsolutePath();
    String assetsDir = parentDir + File.separator + "assets";
    return assetsDir;
  }

  public static String[] getAllCases() {
    File file = new File(Utils.getAssetsDir());
    File[] cases = file.listFiles();
    String[] testcases = new String[cases.length];
    for (int i = 0; i < testcases.length; i++)
      testcases[i] = cases[i].getName();
    return testcases;
  }
  
  public static String getDestDir() {
      File file = new File("");
      String parentDir = file.getAbsolutePath();
      String destDir = parentDir + File.separator + "dest";
      return destDir;
  }

  public static BufferedImage getImage(String testcase, int which) {
    String assetsFolder = getAssetsDir(), filename;

    switch(which) {
    case LEFT:
      filename = LEFT_IMAGE;
      break;
    case RIGHT:
      filename = RIGHT_IMAGE;
      break;
    case BENCHMARK_LEFT:
      filename = LEFT_BENCHMARK;
      break;
    case BENCHMARK_RIGHT:
      filename = RIGHT_BENCHMARK;
      break;
    default:
      filename = "";
    }

    String path = assetsFolder + File.separator + testcase + File.separator + filename;
    File file = new File(path);
    BufferedImage img = null;
    
    try {
      img = ImageIO.read(file);
      int type = img.getType();
      
      if (type != BufferedImage.TYPE_3BYTE_BGR && type != BufferedImage.TYPE_BYTE_GRAY) {
        throw new Exception("Wrong image type.");
      }
    } catch(Exception e) {
      e.printStackTrace();
    }
    
    return img;
  }

  public static int[][] getPixels(BufferedImage image) {
    int type = image.getType();
    int w = image.getWidth();
    int h = image.getHeight();
    byte[] data = ((DataBufferByte)image.getRaster().getDataBuffer()).getData();
    int[][] pixels = new int[h][w];
    
    if (type == BufferedImage.TYPE_3BYTE_BGR) {
      final int pLength = 3;
      for (int p = 0, row = 0, col = 0; p < data.length; p += pLength) {
        int argb = 0;
        argb += -16777216;                        // 255
        argb += ((int) data[p] & 0xff);           // blue
        argb += (((int) data[p+1] & 0xff) << 8);  // green
        argb += (((int) data[p+2] & 0xff) << 16); // red
        pixels[row][col] = argb;
        col++;
        if (col == w) {
          col = 0;
          row++;
        }
      }
    } else if (type == BufferedImage.TYPE_BYTE_GRAY) {
      for (int p = 0, row = 0, col = 0; p < data.length; p++) {
        pixels[row][col] = (int) data[p] & 0xff;
        col++;
        if (col == w) {
          col = 0;
          row++;
        }
      }
    }

    return pixels;
  }

  public static void saveImage(BufferedImage[] image, String testcase, String method) {
    BufferedImage left = image[0], right = image[1];

    try {
      if (left.getType() != BufferedImage.TYPE_BYTE_GRAY || right.getType() != BufferedImage.TYPE_BYTE_GRAY)
        throw new Exception("Wrong image type");
    } catch(Exception e) {
        e.printStackTrace();
    }

    int M = left.getHeight(), N = right.getWidth();
    WritableRaster lr = left.getRaster(), rr = right.getRaster(); 
    
    for (int i = 0; i < M; i++) {
      for (int j = 0; j < N; j++) {
        lr.setSample(j, i, 0, lr.getSample(j, i, 0) * 3);
        rr.setSample(j, i, 0, rr.getSample(j, i, 0) * 3);
      }
    }

    try {
      String path = getDestDir() + File.separator + testcase + File.separator;
      File l = new File(path + testcase + "_disp1_" + method + ".png");
      File r = new File(path + testcase + "_disp5_" + method + ".png");
      l.mkdirs();
      ImageIO.write(left, "PNG", l);
      ImageIO.write(right, "PNG", r);
      System.out.println("Images has been saved.");
    } catch(Exception e) {
      e.printStackTrace();
    }
  }
}
