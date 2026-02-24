"""
CNN Animation for 5-Year-Olds - SIMPLIFIED VERSION
A simple, visual demonstration of how CNNs work.
This version creates individual frames and can save them.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Create output directory for frames
output_dir = "cnn_frames"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ============================================================================
# Create a simple grid "image" (like a cat pixelated)
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

# Simple edge detection kernel (magnifying glass)
kernel = np.array([
    [1, 0, -1],
    [2, 0, -2],
    [1, 0, -1]
], dtype=float)

# ============================================================================
# Generate frames
# ============================================================================

def generate_frame(frame_num, total_frames=20):
    """Generate a single frame of the animation"""
    
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('How Computers Learn to See: Magic Magnifying Glass!',
                 fontsize=18, fontweight='bold', color='purple')
    
    # Subplot 1: Original image
    ax1 = plt.subplot(2, 3, 1)
    ax1.imshow(cat_image, cmap='Greys', vmin=0, vmax=1, interpolation='nearest')
    ax1.set_title('Original Image\n(The Cat Picture)', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(8))
    ax1.set_yticks(range(8))
    ax1.grid(True, alpha=0.3)
    
    # Subplot 2: Magnifying glass sliding
    ax2 = plt.subplot(2, 3, 2)
    
    kernel_size = 3
    stride = 1
    max_positions = 6 * 6
    position_index = int((frame_num / total_frames) * max_positions)
    
    row = (position_index // 6) * stride
    col = (position_index % 6) * stride
    
    ax2.imshow(cat_image, cmap='Greys', vmin=0, vmax=1, interpolation='nearest')
    
    if row + kernel_size <= cat_image.shape[0] and col + kernel_size <= cat_image.shape[1]:
        rect = patches.Rectangle((col-0.5, row-0.5), kernel_size, kernel_size,
                                 linewidth=3, edgecolor='red', facecolor='yellow', alpha=0.3)
        ax2.add_patch(rect)
    
    ax2.set_title('Magnifying Glass Sliding\n(Red Box = Kernel)', fontsize=11, fontweight='bold', color='red')
    ax2.set_xticks(range(8))
    ax2.set_yticks(range(8))
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(-0.5, 7.5)
    ax2.set_ylim(7.5, -0.5)
    
    # Subplot 3: Output feature map
    ax3 = plt.subplot(2, 3, 3)
    
    output_map = np.zeros((6, 6))
    for i in range(position_index + 1):
        out_row = i // 6
        out_col = i % 6
        if out_row < 6 and out_col < 6:
            r = (i // 6) * stride
            c = (i % 6) * stride
            if r + kernel_size <= cat_image.shape[0] and c + kernel_size <= cat_image.shape[1]:
                patch = cat_image[r:r+kernel_size, c:c+kernel_size]
                result = np.sum(patch * kernel)
                output_map[out_row, out_col] = np.clip(result / 10, 0, 1)
    
    im3 = ax3.imshow(output_map, cmap='hot', vmin=0, vmax=1, interpolation='nearest')
    ax3.set_title('Output Feature Map\n(What the Glass Found)', fontsize=11, fontweight='bold')
    ax3.set_xticks(range(6))
    ax3.set_yticks(range(6))
    ax3.grid(True, alpha=0.3, color='white')
    plt.colorbar(im3, ax=ax3, label='Pattern Strength')
    
    # Subplot 4: Layers hierarchy
    ax4 = plt.subplot(2, 3, 4)
    ax4.axis('off')
    
    progress = min(frame_num / total_frames, 1.0)
    layers = [
        ('Layer 1: Find Lines', 0.8),
        ('Layer 2: Find Shapes', 0.6),
        ('Layer 3: Find Features', 0.4),
        ('Layer 4: Recognize Cat!', 0.2),
    ]
    
    for i, (name, y) in enumerate(layers):
        if i < len(layers) * progress:
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
    ax4.set_title('Tower of Learning Layers\n(Building Recognition Step by Step)',
                 fontsize=11, fontweight='bold')
    
    # Subplot 5: Stride explanation
    ax5 = plt.subplot(2, 3, 5)
    ax5.set_xlim(-0.5, 8)
    ax5.set_ylim(-0.5, 4)
    ax5.axis('off')
    
    stride_frame = int((frame_num / total_frames) * 5)
    
    # Grid
    for i in range(8):
        ax5.axvline(i + 0.5, color='gray', linewidth=0.5, alpha=0.5)
    for i in range(4):
        ax5.axhline(i + 0.5, color='gray', linewidth=0.5, alpha=0.5)
    
    # Small hops
    ax5.text(0.5, 3.5, 'Small Hops (Stride=1)', fontsize=10, fontweight='bold',
            ha='center', bbox=dict(boxstyle='round', facecolor='lightblue'))
    for j in range(min(stride_frame + 1, 6)):
        circle = patches.Circle((j + 0.5, 3), 0.2, color='green', alpha=0.7)
        ax5.add_patch(circle)
    
    # Big jumps
    ax5.text(0.5, 1.5, 'Big Jumps (Stride=2)', fontsize=10, fontweight='bold',
            ha='center', bbox=dict(boxstyle='round', facecolor='lightyellow'))
    for j in range(min(stride_frame + 1, 3)):
        circle = patches.Circle((j * 2 + 0.5, 1), 0.2, color='orange', alpha=0.7)
        ax5.add_patch(circle)
    
    ax5.set_title('Stride: How Far the Glass Jumps\n(Frog Hopping!)',
                 fontsize=11, fontweight='bold')
    
    # Subplot 6: Learning progress
    ax6 = plt.subplot(2, 3, 6)
    
    accuracy = 30 + (frame_num / total_frames) * 70
    bar_width = accuracy / 100
    
    rect = patches.Rectangle((0.1, 0.6), bar_width * 0.8, 0.15,
                            edgecolor='black', facecolor='lightgreen')
    ax6.add_patch(rect)
    rect_bg = patches.Rectangle((0.1, 0.6), 0.8, 0.15,
                               edgecolor='black', facecolor='none', linewidth=2)
    ax6.add_patch(rect_bg)
    ax6.text(0.5, 0.675, f'{accuracy:.0f}% Learned!',
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    learning_texts = [
        'Picture 1: Is this a cat?',
        'Picture 2: How about this?',
        'Picture 3: And this one?',
        'After 100 pictures...',
        'After 1000 pictures...',
        'I learned what cats look like!',
        'I can recognize ANY cat now!',
    ]
    
    text_idx = min(int((frame_num / total_frames) * len(learning_texts)), len(learning_texts) - 1)
    ax6.text(0.5, 0.4, learning_texts[text_idx],
            ha='center', va='center', fontsize=11, fontweight='bold', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    ax6.set_xlim(0, 1)
    ax6.set_ylim(0, 1)
    ax6.axis('off')
    ax6.set_title('Learning from Examples\n(Training the Computer)',
                 fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    return fig

# Generate a few key frames
print("Generating animation frames...")
frames_to_generate = [0, 5, 10, 15, 20]

for frame_num in frames_to_generate:
    print(f"  Generating frame {frame_num}...", end=" ")
    fig = generate_frame(frame_num, total_frames=20)
    filename = os.path.join(output_dir, f"cnn_frame_{frame_num:02d}.png")
    fig.savefig(filename, dpi=100, bbox_inches='tight')
    print(f"Saved to {filename}")
    plt.close(fig)

print("\n✓ Frames saved to 'cnn_frames/' directory!")
print("\nTo run the full animation interactively:")
print("  python cnn_animator.py")
print("\nTo view sample frames:")
print("  Open the files in cnn_frames/ folder")
