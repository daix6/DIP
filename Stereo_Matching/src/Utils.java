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

  public static String getDestDir() {
    File file = new File("");
    String parentDir = file.getAbsolutePath();
    String destDir = parentDir + File.separator + "dest";
    return destDir;
  }

  public static String[] getAllCases() {
    File file = new File(Utils.getAssetsDir());
    File[] cases = file.listFiles();
    String[] testcases = new String[cases.length];
    for (int i = 0; i < testcases.length; i++)
      testcases[i] = cases[i].getName();
    return testcases;
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
    int w = image.getWidth(), h = image.getHeight();
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
    } else
      System.err.println("Wrong image type");

    return pixels;
  }

  public static double[][] getIntensity(BufferedImage image) {
    int type = image.getType();
    int w = image.getWidth(),  h = image.getHeight();
    byte[] data = ((DataBufferByte)image.getRaster().getDataBuffer()).getData();
    double[][] intensity = new double[h][w];

    if (type == BufferedImage.TYPE_3BYTE_BGR) {
      for (int p = 0, row = 0, col = 0; p < data.length; p += 3) {
        int B = (int) data[p] & 0xff;           // blue
        int G = (int) data[p+1] & 0xff;         // green
        int R = (int) data[p+2] & 0xff;         // red
        intensity[row][col] = 0.2989 * R + 0.5870 * G + 0.1140 * B;
        col++;
        if (col == w) {
          col = 0;
          row++;
        }
      }
    } else if (type == BufferedImage.TYPE_BYTE_GRAY) {
      for (int p = 0, row = 0, col = 0; p < data.length; p++) {
        intensity[row][col] = (int) data[p] & 0xff;
        col++;
        if (col == w) {
          col = 0;
          row++;
        }
      }
    } else
        System.err.println("Wrong image type");

    return intensity;
  }

  public static BufferedImage addIntensity(BufferedImage image, double intensity) {
    int w = image.getWidth(), h = image.getHeight();

    double[][] inten = Utils.getIntensity(image);
    double[] added = new double[w*h];

    for (int i = 0; i < h; i++)
      for (int j = 0; j < w; j++)
        added[i*w + j] = inten[i][j] + intensity;

    BufferedImage modified = new BufferedImage(w, h, BufferedImage.TYPE_BYTE_GRAY);
    modified.getRaster().setPixels(0, 0, w, h, added);

    return modified;
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

  public static double rgb2gray(int rgb) {
    int R = ((int)(rgb >> 16)) & 0xff,
        G = ((int)(rgb >> 8)) & 0xff,
        B = ((int)rgb) & 0xff;

    return 0.2989 * R + 0.5870 * G + 0.1140 * B;
  }

  public static int[][] rgb2lab(int[][] image) {
    int M = image.length, N = image[0].length;
    int[][] labs = new int[M][N];
    for (int i = 0; i < M; i++) {
      for (int j = 0; j < N; j++) {
        int pixel = image[i][j];

        double r, g, b, X, Y, Z, fx, fy, fz, xr, yr, zr;
        double Ls, as, bs;
        double eps = 216.f/24389.f;
        double k = 24389.f/27.f;

        double Xr =0.964221f;  // reference white D50
        double Yr = 1.0f;
        double Zr = 0.825211f;

        // To [0,1]
        r = (((int)pixel >> 16) & 0xff) / 255.f;
        g = (((int)pixel >> 8) & 0xff) / 255.f;
        b = (((int)pixel) & 0xff) / 255.f;

        // assuming sRGB (D65)
        if (r <= 0.04045)
          r = r/12;
        else
          r = (double) Math.pow((r + 0.055)/1.055, 2.4);

        if (g <= 0.04045)
          g = g/12;
       else
          g = (double) Math.pow((g + 0.055)/1.055, 2.4);

        if (b <= 0.04045)
          b = r/12;
        else
          b = (double) Math.pow((b + 0.055)/1.055, 2.4);

        // RGB TO XYZ
        X = 0.436052025f * r + 0.385081593f * g + 0.143087414f * b;
        Y = 0.222491598f * r + 0.71688606f  * g + 0.060621486f * b;
        Z = 0.013929122f * r + 0.097097002f * g + 0.71418547f  * b;

        // XYZ TO LAB
        xr = X/Xr;
        yr = Y/Yr;
        zr = Z/Zr;

        if (xr > eps)
          fx = (double) Math.pow(xr, 1/3.);
        else
          fx = (double) ((k * xr + 16.) / 116.);

        if (yr > eps)
          fy = (double) Math.pow(yr, 1/3.);
        else
          fy = (double) ((k * yr + 16.) / 116.);

        if (zr > eps)
          fz = (double) Math.pow(zr, 1/3.);
        else
          fz = (double) ((k * zr + 16.) / 116.);

        Ls = (116 * fy) - 16;
        as = 500 * (fx - fy);
        bs = 200 * (fy - fz);

        // All scale to [0,255]
        labs[i][j] = ((int)(2.55*Ls + .5) << 16) + ((int)(as + 128.5) << 8) + ((int)(bs + 128.5));
      }
    }

    return labs;
  }
}
