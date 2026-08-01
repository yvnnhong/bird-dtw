import sys
from pathlib import Path

# Add src to path to import bird_dtw
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bird_dtw import DTW

def test_dtw_sanity_check():
    """Test DTW against the known walkthrough values"""
    A = [(0, 1), (2, 2), (3, 3)]  # individual path
    B = [(0, 0), (1, 1), (2, 2)]  # template path
    W = 2  # window
    
    dtw = DTW(A, B, W)
    distance, _ = dtw.dynamic_time_warping()
    
    # From your sanity check: final distance should be 3.414
    assert abs(distance - 3.414) < 0.01, f"Expected ~3.414, got {distance}"
    print(f"DTW distance correct: {distance}")

if __name__ == "__main__":
    test_dtw_sanity_check()
    print("All tests passed!")