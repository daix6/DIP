import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;

public class StereoMatching {
  public BufferedImage left, right;
  public BufferedImage disp_l, disp_r;
  public int max_d, patch;
  private double[] badRate;
  
  public StereoMatching(BufferedImage left, BufferedImage right) {
    this(left, right, 79, 5);
  }
  
  public StereoMatching(BufferedImage left, BufferedImage right, int max_disparity, int patch) {
    this.left = left;
    this.right = right;
    this.max_d = max_disparity;
    this.patch = patch;
  }

  public void ssd() {
    int[][] left = Utils.getPixels(this.left),
            right = Utils.getPixels(this.right);
    
    int M = left.length, N = left[0].length; // M-Height, N-Width

    this.disp_l = new BufferedImage(N, M, BufferedImage.TYPE_BYTE_GRAY);
    this.disp_r = new BufferedImage(N, M, BufferedImage.TYPE_BYTE_GRAY);

    for (int i = 0; i < M; i++) {
      for (int j = 0; j < N; j++) {
        int[][] lp = getPatch(left, i, j);
        int[][] rp = getPatch(right, i, j);

        // For left eye image disparity map
        double cost = Double.POSITIVE_INFINITY;
        int min_d = 0;
        for (int d = 0; d < this.max_d; d++) {
          int[][] rp_d = getPatch(right, i, j - d);
          double ssdcost = ssdCost(lp, rp_d);
          if (ssdcost < cost) {
            cost = ssdcost;
            min_d = d;
          }
        }
        this.disp_l.setRGB(j, i, min_d);

        // For right eye image disparity map
        cost = Double.POSITIVE_INFINITY;
        min_d = 0;
        for (int d = 0; d < this.max_d; d++) {
          int[][] lp_d = getPatch(left, i, j + d);
          double ssdcost = ssdCost(rp, lp_d);
          if (ssdcost < cost) {
            cost = ssdcost;
            min_d = d;
          }
        }
        this.disp_r.setRGB(j, i, Utils.toRGB(min_d));
      }
    }
  }

  // Cost Evaluation
  private double ssdCost(int[][] left, int[][] right) {
    double cost = 0;
    for (int i = 0; i < this.patch; i++) {
      for (int j = 0; j < this.patch; j++) {
        cost += Math.pow(Math.abs(left[i][j] - right[i][j]), 2);
      }
    }
    return cost;
  }

  // Helper
  public void evaluate(BufferedImage benchmark_left, BufferedImage benchmark_right) {
    try {
      if (this.disp_l.getType() != BufferedImage.TYPE_BYTE_GRAY || this.disp_r.getType() != BufferedImage.TYPE_BYTE_GRAY) {
        throw new Exception("Wrong image type.");
      }
    
      int[][] l = Utils.getPixels(this.disp_l), r = Utils.getPixels(this.disp_r);
      int[][] bpL = Utils.getPixels(benchmark_left), bpR = Utils.getPixels(benchmark_right);
      
      int M = benchmark_left.getHeight(), N = benchmark_right.getWidth();

      int[] bad= new int[] {0,0};
      for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
          System.out.println(l[i][j] + " " + bpL[i][j]);
          if (Math.abs(l[i][j] - bpL[i][j] / 3.0) > 1)
            bad[0]++;
          if (Math.abs(r[i][j] - bpR[i][j] / 3.0) > 1)
            bad[1]++;
        }
      }

      this.badRate = new double[]{((float)bad[0]) / (M * N), ((float)bad[1]) / (M * N)};
    } catch(Exception e) {
      e.printStackTrace();
    }
  }
  
  public void printBad(String testcase) {
    System.out.println("The bad pixels rate of " + testcase);
    System.out.print(this.badRate[0]);
    System.out.print(" ");
    System.out.println(this.badRate[1]);
  }

  private int[][] getPatch(int[][] pixels, int x, int y) {
    int[][] patch = new int[this.patch][this.patch];
    int M = pixels.length, N = pixels[0].length;
    int pad = this.patch / 2;

    for (int i = x - pad; i < x + pad + 1; i++) {
      for (int j = y - pad; j < y + pad + 1; j++) {
        if (i >= 0 && j >= 0 && i < M && j < N)
          patch[i - x + pad][j - y + pad] = pixels[i][j];
        else
          patch[i - x + pad][j - y + pad] = 0;
      }
    }
    
    return patch;
  }
}
