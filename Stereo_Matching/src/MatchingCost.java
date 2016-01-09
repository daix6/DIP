/**
 * @author Shawn Dai
 * MatchingCost, an interface that provides ways to compute matching cost of two support window
 */
public interface MatchingCost {
  /** Require RGB only
   * @param left support window with rgb value
   * @param right support window with rgb value
   * @return the computed cost
   */
  public double matchingCost(double[][] left, double[][] right);

  /** Require both RGB and LAB
   * @param left support window with rgb value
   * @param right support window with rgb value
   * @param leftLab support window with lab value
   * @param rightLab support window with lab value
   * @return the computed cost
   */
  public double matchingCostLab(int[][] left, int[][] right, int[][] leftLab, int[][] rightLab);
}
