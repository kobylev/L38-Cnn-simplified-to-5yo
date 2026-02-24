"""
CNN Animation for 5-Year-Olds
A simple, visual demonstration of how CNNs work using matplotlib animations.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
from PIL import Image
import io

# Set up the figure and subplots
fig = plt.figure(figsize=(16, 10))
fig.suptitle('🧠 How Computers Learn to See: Magic Magnifying Glass! 🔍', 
             fontsize=18, fontweight='bold', color='purple')

# Create subplots
ax1 = plt.subplot(2, 3, 1)  # Original image
ax2 = plt.subplot(2, 3, 2)  # Magnifying glass sliding
ax3 = plt.subplot(2, 3, 3)  # Output feature map
ax4 = plt.subplot(2, 3, 4)  # Layer visualization
ax5 = plt.subplot(2, 3, 5)  # Stride explanation
ax6 = plt.subplot(2, 3, 6)  # Learning progress

# ============================================================================
# PART 1: Create a simple grid "image" (like a cat pixelated)
# ============================================================================

def create_simple_cat():
    """Create a simple 8x8 'cat' image using numbers"""
    cat = np.array([
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ], dtype=float)
    return cat

cat_image = create_simple_cat()

# ============================================================================
# PART 2: Convolution Kernel (Magic Magnifying Glass)
# ============================================================================

# Simple edge detection kernel
kernel = np.array([
    [1, 0, -1],
    [2, 0, -2],
    [1, 0, -1]
], dtype=float)

# Normalize kernel for display
kernel_display = (kernel - kernel.min()) / (kernel.max() - kernel.min())

# ============================================================================
# PART 3: Animation Setup
# ============================================================================

total_frames = 100
kernel_size = 3

class CNNAnimator:
    def __init__(self):
        self.frame = 0
        self.output_maps = []
        self.positions = []
        self.output_feature_map = np.zeros((6, 6))
        self.learning_progress = []
        
    def compute_convolution_step(self, row, col, stride=1):
        """Compute one step of convolution"""
        patch = cat_image[row:row+kernel_size, col:col+kernel_size]
        result = np.sum(patch * kernel)
        # Normalize to 0-1 range for visualization
        return np.clip(result / 10, 0, 1)
    
    def update(self, frame_num):
        """Update all subplots for animation"""
        self.frame = frame_num
        
        # ====================================================================
        # Subplot 1: Original Image (Static)
        # ====================================================================
        ax1.clear()
        im1 = ax1.imshow(cat_image, cmap='Greys', vmin=0, vmax=1, interpolation='nearest')
        ax1.set_title('📸 Original Image\n(The Cat Picture)', fontsize=12, fontweight='bold')
        ax1.set_xticks(range(8))
        ax1.set_yticks(range(8))
        ax1.grid(True, alpha=0.3)
        
        # ====================================================================
        # Subplot 2: Magnifying Glass Sliding (The Main Show!)
        # ====================================================================
        ax2.clear()
        
        # Calculate which position we're at
        stride = 1
        max_positions = 6 * 6  # 6x6 output for 8x8 input with 3x3 kernel
        position_index = int((self.frame / total_frames) * max_positions)
        
        row = (position_index // 6) * stride
        col = (position_index % 6) * stride
        
        # Make sure we don't go out of bounds
        if row + kernel_size <= cat_image.shape[0] and col + kernel_size <= cat_image.shape[1]:
            # Draw the image
            im2 = ax2.imshow(cat_image, cmap='Greys', vmin=0, vmax=1, interpolation='nearest')
            
            # Draw the magnifying glass (kernel window)
            rect = patches.Rectangle((col-0.5, row-0.5), kernel_size, kernel_size,
                                     linewidth=3, edgecolor='red', facecolor='yellow', alpha=0.3)
            ax2.add_patch(rect)
            
            # Highlight the kernel pattern
            kernel_label = f"🔍 Magnifying Glass\nAt position ({row}, {col})"
            ax2.set_title(kernel_label, fontsize=11, fontweight='bold', color='red')
            
            # Compute and store the result
            result = self.compute_convolution_step(row, col)
            if position_index < len(self.output_feature_map.flatten()):
                out_row = position_index // 6
                out_col = position_index % 6
                self.output_feature_map[out_row, out_col] = result
        
        ax2.set_xticks(range(8))
        ax2.set_yticks(range(8))
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(-0.5, 7.5)
        ax2.set_ylim(7.5, -0.5)
        
        # ====================================================================
        # Subplot 3: Output Feature Map (What the glass found)
        # ====================================================================
        ax3.clear()
        im3 = ax3.imshow(self.output_feature_map, cmap='hot', vmin=0, vmax=1, interpolation='nearest')
        ax3.set_title('🎯 What the Magnifying Glass Found\n(Feature Map)', 
                     fontsize=11, fontweight='bold')
        ax3.set_xticks(range(6))
        ax3.set_yticks(range(6))
        ax3.grid(True, alpha=0.3, color='white')
        plt.colorbar(im3, ax=ax3, label='Pattern Strength')
        
        # ====================================================================
        # Subplot 4: Layers (Hierarchy of Learning)
        # ====================================================================
        ax4.clear()
        ax4.axis('off')
        
        # Draw the tower of layers
        layer_info = [
            ('Layer 1\n🔍 Find Lines', 0.8),
            ('Layer 2\n⬜ Find Shapes', 0.6),
            ('Layer 3\n👁️ Find Features', 0.4),
            ('Layer 4\n🐱 Recognize Cat!', 0.2),
        ]
        
        progress = min(self.frame / total_frames, 1.0)
        
        for i, (name, y) in enumerate(layer_info):
            if i < len(layer_info) * progress:
                color = 'lightgreen'
                alpha = 1.0
            else:
                color = 'lightgray'
                alpha = 0.5
            
            rect = patches.FancyBboxPatch((0.1, y-0.08), 0.8, 0.12,
                                         boxstyle="round,pad=0.01",
                                         edgecolor='black', facecolor=color, alpha=alpha)
            ax4.add_patch(rect)
            ax4.text(0.5, y, name, ha='center', va='center', fontsize=10, fontweight='bold')
        
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)
        ax4.set_title('🏗️ Tower of Learning Layers\n(Building Recognition Step by Step)', 
                     fontsize=11, fontweight='bold')
        
        # ====================================================================
        # Subplot 5: Stride Explanation (Frog Jumping)
        # ====================================================================
        ax5.clear()
        ax5.set_xlim(-0.5, 8)
        ax5.set_ylim(-0.5, 4)
        ax5.axis('off')
        
        # Draw stride visualization
        stride_frame = int((self.frame / total_frames) * 5)
        
        # Draw grid
        for i in range(8):
            ax5.axvline(i + 0.5, color='gray', linewidth=0.5, alpha=0.5)
        for i in range(4):
            ax5.axhline(i + 0.5, color='gray', linewidth=0.5, alpha=0.5)
        
        # Small jumps (stride=1)
        ax5.text(0.5, 3.5, '🐸 Small Hops (Stride=1)', fontsize=10, fontweight='bold', 
                ha='center', bbox=dict(boxstyle='round', facecolor='lightblue'))
        for j in range(min(stride_frame + 1, 6)):
            circle = patches.Circle((j + 0.5, 3), 0.2, color='green', alpha=0.7)
            ax5.add_patch(circle)
        
        # Big jumps (stride=2)
        ax5.text(0.5, 1.5, '🐸 Big Jumps (Stride=2)', fontsize=10, fontweight='bold',
                ha='center', bbox=dict(boxstyle='round', facecolor='lightyellow'))
        for j in range(min(stride_frame + 1, 3)):
            circle = patches.Circle((j * 2 + 0.5, 1), 0.2, color='orange', alpha=0.7)
            ax5.add_patch(circle)
        
        ax5.set_title('🐸 Stride: How Far the Glass Jumps', fontsize=11, fontweight='bold')
        
        # ====================================================================
        # Subplot 6: Learning Progress
        # ====================================================================
        ax6.clear()
        
        # Simulate learning progress
        accuracy = 30 + (self.frame / total_frames) * 70  # 30% to 100%
        
        # Draw progress bar
        bar_width = accuracy / 100
        rect = patches.Rectangle((0.1, 0.6), bar_width * 0.8, 0.15,
                                edgecolor='black', facecolor='lightgreen')
        ax6.add_patch(rect)
        rect_bg = patches.Rectangle((0.1, 0.6), 0.8, 0.15,
                                   edgecolor='black', facecolor='none', linewidth=2)
        ax6.add_patch(rect_bg)
        ax6.text(0.5, 0.675, f'{accuracy:.0f}% Learned! 📚', ha='center', va='center',
                fontsize=12, fontweight='bold')
        
        # Learning text
        learning_texts = [
            '📸 Picture 1: Is this a cat?',
            '📸 Picture 2: How about this?',
            '📸 Picture 3: And this one?',
            '✅ After 1000 pictures...',
            '🎓 I learned what cats look like!',
            '🐱 I can recognize ANY cat now!'
        ]
        
        text_idx = min(int((self.frame / total_frames) * len(learning_texts)), len(learning_texts) - 1)
        ax6.text(0.5, 0.4, learning_texts[text_idx], ha='center', va='center',
                fontsize=11, fontweight='bold', style='italic',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        ax6.set_xlim(0, 1)
        ax6.set_ylim(0, 1)
        ax6.axis('off')
        ax6.set_title('📚 Learning from Examples\n(Training the Computer)', 
                     fontsize=11, fontweight='bold')
        
        return [ax1, ax2, ax3, ax4, ax5, ax6]

# Create animator
animator_obj = CNNAnimator()

# ============================================================================
# PART 4: Create Animation
# ============================================================================

def animate(frame):
    return animator_obj.update(frame)

anim = FuncAnimation(fig, animate, frames=total_frames, interval=100, blit=False)

# Adjust layout and save
plt.tight_layout()

# Add text explaining what's happening
fig.text(0.5, 0.02, 
         '🔍 Watch the magic magnifying glass (red box) slide across the cat picture!\n' +
         'It finds patterns and creates a smaller map of what it found. ' +
         'This happens in layers!',
         ha='center', fontsize=11, style='italic', wrap=True,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

print("🎬 Animation starting... Watch the CNN learn!")
print("🔍 The red box is the 'magic magnifying glass' (kernel) looking for patterns")
print("📊 The output shows what patterns were found in the image")
plt.show()
