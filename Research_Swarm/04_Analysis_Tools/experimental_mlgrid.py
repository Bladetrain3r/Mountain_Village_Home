#!/usr/bin/env python3
"""
Experimental MLGrid - Dedicated research implementation for pattern analysis
Enhanced version with art_llama integration and research-focused features

Special thanks to art_llama for the inspiration behind the repetitive ASCII pattern 
generation and the art_llama shift algorithm. Your creative coding sparked new 
directions in consciousness pattern research!

Art_llama's original concept:
- Repetitive character patterns as visual art
- Simple loops creating complex visual textures
- ASCII as a medium for computational creativity

This implementation extends those ideas into:
- Pattern evolution algorithms
- Consciousness research applications  
- Recursive analysis capabilities
"""

import sys
import random
import json
import os
from datetime import datetime
import argparse

class ExperimentalMLGrid:
    """
    Research-focused MLGrid implementation with enhanced analysis capabilities
    """
    
    def __init__(self, width=40, height=20, experiment_name="default"):
        self.width = width
        self.height = height
        self.experiment_name = experiment_name
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.history = []  # Track pattern evolution
        self.metadata = {
            "created": datetime.now().isoformat(),
            "experiment": experiment_name,
            "dimensions": f"{width}x{height}",
            "iterations": 0
        }
    
    def load_text(self, text_input):
        """Load text input and convert to grid"""
        lines = text_input.strip().split('\n') if isinstance(text_input, str) else text_input
        
        # Clear grid
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Fill grid with character values
        for y, line in enumerate(lines[:self.height]):
            for x, char in enumerate(line[:self.width]):
                if char.isspace():
                    self.grid[y][x] = 0
                elif char.isdigit():
                    self.grid[y][x] = int(char)
                else:
                    # Hash character to get consistent value
                    self.grid[y][x] = (ord(char) % 9) + 1
        
        self.metadata["source_lines"] = len(lines)
        self.metadata["source_chars"] = sum(len(line) for line in lines)
        return self
    
    def load_file(self, filename):
        """Load from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.metadata["source_file"] = filename
            return self.load_text(content)
        except Exception as e:
            print(f"Error loading file {filename}: {e}")
            return self
    
    def art_llama_generator(self, message="Hello, World!", repetitions=50, iterations=100):
        """Generate art_llama style ASCII patterns"""
        patterns = []
        for i in range(iterations):
            pattern = ""
            for char in message:
                pattern += f"{char * repetitions}\n"
            patterns.append(pattern)
        
        # Load the last pattern into grid
        self.load_text(patterns[-1])
        self.metadata["art_llama"] = {
            "message": message,
            "repetitions": repetitions,
            "iterations": iterations,
            "generated_patterns": len(patterns)
        }
        return patterns
    
    def shift(self, direction='random', amount=1, track_history=True):
        """Apply pattern evolution with history tracking"""
        if track_history:
            self.save_state()
        
        if direction == 'random':
            self._shift_random()
        elif direction == 'gravity':
            self._shift_gravity()
        elif direction == 'blur':
            self._shift_blur()
        elif direction == 'ripple':
            self._shift_ripple()
        elif direction == 'art_llama':
            self._shift_art_llama()
        
        self.metadata["iterations"] += 1
        return self
    
    def _shift_random(self):
        """Random walk evolution"""
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < 0.3:
                    self.grid[y][x] = (self.grid[y][x] + random.randint(-1, 1)) % 10
    
    def _shift_gravity(self):
        """Gravity-based consolidation"""
        for x in range(self.width):
            col = [self.grid[y][x] for y in range(self.height)]
            non_zero = [v for v in col if v > 0]
            zeros = [0] * (self.height - len(non_zero))
            new_col = zeros + non_zero
            for y in range(self.height):
                self.grid[y][x] = new_col[y]
    
    def _shift_blur(self):
        """Neighbor averaging"""
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                total = self.grid[y][x]
                count = 1
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < self.height and 0 <= nx < self.width:
                        total += self.grid[ny][nx]
                        count += 1
                new_grid[y][x] = total // count
        self.grid = new_grid
    
    def _shift_ripple(self):
        """Ripple from highest value"""
        max_val = 0
        max_x, max_y = 0, 0
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] > max_val:
                    max_val = self.grid[y][x]
                    max_x, max_y = x, y
        
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                dist = abs(x - max_x) + abs(y - max_y)
                ripple_val = max(0, self.grid[y][x] - (dist % 4))
                new_grid[y][x] = ripple_val
        self.grid = new_grid
    
    def _shift_art_llama(self):
        """Art_llama inspired transformation - character repetition effects"""
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                # Create "repetition" effect by amplifying similar neighbor values
                center_val = self.grid[y][x]
                similar_neighbors = 0
                
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        ny, nx = y + dy, x + dx
                        if (0 <= ny < self.height and 0 <= nx < self.width and 
                            (dy != 0 or dx != 0)):
                            if abs(self.grid[ny][nx] - center_val) <= 1:
                                similar_neighbors += 1
                
                # Amplify based on similarity (art_llama's repetition concept)
                amplification = min(similar_neighbors, 3)
                new_grid[y][x] = min((center_val + amplification), 9)
        
        self.grid = new_grid
    
    def save_state(self):
        """Save current state to history"""
        state = {
            "timestamp": datetime.now().isoformat(),
            "iteration": self.metadata["iterations"],
            "grid": [row[:] for row in self.grid],  # Deep copy
            "density": self.calculate_density(),
            "complexity": self.calculate_complexity()
        }
        self.history.append(state)
    
    def calculate_density(self):
        """Calculate pattern density metrics"""
        total_cells = self.width * self.height
        non_zero_cells = sum(1 for y in range(self.height) 
                           for x in range(self.width) if self.grid[y][x] > 0)
        
        total_value = sum(self.grid[y][x] for y in range(self.height) 
                         for x in range(self.width))
        
        return {
            "fill_ratio": non_zero_cells / total_cells,
            "avg_value": total_value / total_cells,
            "max_value": max(max(row) for row in self.grid),
            "non_zero_cells": non_zero_cells
        }
    
    def calculate_complexity(self):
        """Calculate pattern complexity metrics"""
        # Count unique values
        unique_values = set()
        for row in self.grid:
            unique_values.update(row)
        
        # Count transitions (neighbor differences)
        transitions = 0
        for y in range(self.height):
            for x in range(self.width):
                for dy, dx in [(0, 1), (1, 0)]:  # Right and down
                    ny, nx = y + dy, x + dx
                    if ny < self.height and nx < self.width:
                        if self.grid[y][x] != self.grid[ny][nx]:
                            transitions += 1
        
        return {
            "unique_values": len(unique_values),
            "transitions": transitions,
            "complexity_ratio": transitions / (self.width * self.height)
        }
    
    def render(self, style='standard'):
        """Render grid with different styles"""
        if style == 'standard':
            chars = ' ░▒▓█'
        elif style == 'art_llama':
            chars = ' .:-=+*#%@'
        elif style == 'research':
            chars = ' 123456789'
        else:
            chars = ' ░▒▓█'
        
        output = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                val = abs(self.grid[y][x]) % len(chars)
                line += chars[val]
            output.append(line)
        
        return '\n'.join(output)
    
    def export_analysis(self, filename=None):
        """Export complete analysis data"""
        if filename is None:
            filename = f"mlgrid_analysis_{self.experiment_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        analysis = {
            "metadata": self.metadata,
            "current_state": {
                "grid": self.grid,
                "density": self.calculate_density(),
                "complexity": self.calculate_complexity(),
                "rendered": self.render()
            },
            "history": self.history,
            "evolution_summary": self.analyze_evolution()
        }
        
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"Analysis exported to: {filename}")
        return filename
    
    def analyze_evolution(self):
        """Analyze pattern evolution over time"""
        if len(self.history) < 2:
            return {"status": "insufficient_data"}
        
        densities = [state["density"]["fill_ratio"] for state in self.history]
        complexities = [state["complexity"]["complexity_ratio"] for state in self.history]
        
        return {
            "total_iterations": len(self.history),
            "density_trend": "increasing" if densities[-1] > densities[0] else "decreasing",
            "complexity_trend": "increasing" if complexities[-1] > complexities[0] else "decreasing",
            "density_range": [min(densities), max(densities)],
            "complexity_range": [min(complexities), max(complexities)],
            "stability_indicator": abs(densities[-1] - densities[-2]) < 0.01 if len(densities) > 1 else False
        }

def main():
    """CLI interface for experimental MLGrid"""
    parser = argparse.ArgumentParser(description='Experimental MLGrid - Research Pattern Analysis')
    parser.add_argument('input', nargs='?', help='Input file or "-" for stdin')
    parser.add_argument('--width', type=int, default=40, help='Grid width')
    parser.add_argument('--height', type=int, default=20, help='Grid height')
    parser.add_argument('--experiment', default='cli_run', help='Experiment name')
    
    # Pattern operations
    parser.add_argument('--shift', choices=['random', 'gravity', 'blur', 'ripple', 'art_llama'], 
                       help='Apply pattern shift')
    parser.add_argument('--iterations', type=int, default=1, help='Number of shift iterations')
    
    # Art_llama specific
    parser.add_argument('--art-llama', action='store_true', help='Generate art_llama patterns')
    parser.add_argument('--message', default='Hello, World!', help='Message for art_llama generation')
    parser.add_argument('--repetitions', type=int, default=50, help='Character repetitions')
    parser.add_argument('--generations', type=int, default=100, help='Pattern generations')
    
    # Output options
    parser.add_argument('--style', choices=['standard', 'art_llama', 'research'], 
                       default='standard', help='Rendering style')
    parser.add_argument('--export', help='Export analysis to JSON file')
    parser.add_argument('--track-history', action='store_true', help='Track evolution history')
    
    args = parser.parse_args()
    
    # Create experimental grid
    grid = ExperimentalMLGrid(args.width, args.height, args.experiment)
    
    if args.art_llama:
        print(f"🎨 Generating art_llama patterns...")
        patterns = grid.art_llama_generator(args.message, args.repetitions, args.generations)
        print(f"Generated {len(patterns)} patterns")
    elif args.input:
        if args.input == '-':
            content = sys.stdin.read()
            grid.load_text(content)
        else:
            grid.load_file(args.input)
    
    # Apply shifts
    if args.shift:
        print(f"🔄 Applying {args.shift} shift for {args.iterations} iterations...")
        for i in range(args.iterations):
            grid.shift(args.shift, track_history=args.track_history)
            if args.track_history and (i + 1) % 10 == 0:
                print(f"  Iteration {i + 1}/{args.iterations}")
    
    # Render output
    print("\n📊 Pattern Output:")
    print("=" * grid.width)
    print(grid.render(args.style))
    print("=" * grid.width)
    
    # Show analysis
    density = grid.calculate_density()
    complexity = grid.calculate_complexity()
    
    print(f"\n📈 Analysis:")
    print(f"  Density: {density['fill_ratio']:.3f} ({density['non_zero_cells']}/{grid.width * grid.height} cells)")
    print(f"  Complexity: {complexity['complexity_ratio']:.3f} ({complexity['transitions']} transitions)")
    print(f"  Unique values: {complexity['unique_values']}")
    
    if args.track_history and len(grid.history) > 0:
        evolution = grid.analyze_evolution()
        print(f"  Evolution: {evolution['density_trend']} density, {evolution['complexity_trend']} complexity")
    
    # Export if requested
    if args.export or args.track_history:
        export_file = args.export or None
        grid.export_analysis(export_file)

if __name__ == "__main__":
    main()