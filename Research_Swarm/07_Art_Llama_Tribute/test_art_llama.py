#!/usr/bin/env python3
"""
Test script for art_llama MLGrid integration
Demonstrates the experimental features
"""

from experimental_mlgrid import ExperimentalMLGrid
import json

def test_art_llama_basic():
    """Test basic art_llama pattern generation"""
    print("🎨 Testing Art_Llama Basic Pattern Generation")
    print("=" * 60)
    
    grid = ExperimentalMLGrid(width=60, height=15, experiment_name="art_llama_test")
    
    # Generate art_llama style patterns
    patterns = grid.art_llama_generator("Hello, World!", repetitions=4, iterations=5)
    
    print("Generated Pattern:")
    print(grid.render('art_llama'))
    
    density = grid.calculate_density()
    print(f"\nDensity Analysis: {density['fill_ratio']:.3f} fill ratio")
    
    return grid

def test_art_llama_evolution():
    """Test art_llama pattern evolution"""
    print("\n🔄 Testing Art_Llama Pattern Evolution")
    print("=" * 60)
    
    grid = ExperimentalMLGrid(width=40, height=10, experiment_name="art_llama_evolution")
    
    # Start with art_llama pattern
    grid.art_llama_generator("Hi AI!", repetitions=8, iterations=3)
    
    print("Initial art_llama pattern:")
    print(grid.render('standard'))
    
    # Apply art_llama specific transformation
    print("\nAfter art_llama shift:")
    grid.shift('art_llama', track_history=True)
    print(grid.render('standard'))
    
    # Apply traditional shifts
    print("\nAfter gravity shift:")
    grid.shift('gravity', track_history=True)
    print(grid.render('standard'))
    
    print("\nAfter blur shift:")
    grid.shift('blur', track_history=True)
    print(grid.render('standard'))
    
    # Show evolution analysis
    evolution = grid.analyze_evolution()
    print(f"\nEvolution Summary: {json.dumps(evolution, indent=2)}")
    
    return grid

def test_recursive_analysis():
    """Test recursive MLGrid analysis"""
    print("\n🌀 Testing Recursive MLGrid Analysis")
    print("=" * 60)
    
    # Create first grid with art_llama pattern
    grid1 = ExperimentalMLGrid(width=30, height=8, experiment_name="recursive_test_1")
    grid1.art_llama_generator("Recursive", repetitions=3, iterations=2)
    pattern1 = grid1.render('research')
    
    print("First grid pattern:")
    print(pattern1)
    
    # Feed first pattern into second grid
    grid2 = ExperimentalMLGrid(width=30, height=8, experiment_name="recursive_test_2")
    grid2.load_text(pattern1)
    
    print("\nSecond grid (loaded from first):")
    print(grid2.render('research'))
    
    # Apply transformations to second grid
    grid2.shift('ripple')
    
    print("\nSecond grid after ripple:")
    print(grid2.render('research'))
    
    # Compare densities
    density1 = grid1.calculate_density()
    density2 = grid2.calculate_density()
    
    print(f"\nDensity Comparison:")
    print(f"  Grid 1: {density1['fill_ratio']:.3f}")
    print(f"  Grid 2: {density2['fill_ratio']:.3f}")
    print(f"  Difference: {abs(density1['fill_ratio'] - density2['fill_ratio']):.3f}")
    
    return grid1, grid2

def demonstrate_all_shifts():
    """Demonstrate all shift types on art_llama input"""
    print("\n⚡ Demonstrating All Shift Types")
    print("=" * 60)
    
    base_message = "MLGrid!"
    
    shift_types = ['random', 'gravity', 'blur', 'ripple', 'art_llama']
    
    for shift_type in shift_types:
        print(f"\n--- {shift_type.upper()} SHIFT ---")
        
        grid = ExperimentalMLGrid(width=35, height=6, experiment_name=f"demo_{shift_type}")
        grid.art_llama_generator(base_message, repetitions=5, iterations=1)
        
        print("Before:")
        print(grid.render('standard'))
        
        grid.shift(shift_type)
        
        print("After:")
        print(grid.render('standard'))
        
        density = grid.calculate_density()
        complexity = grid.calculate_complexity()
        print(f"Stats: Density {density['fill_ratio']:.3f}, Complexity {complexity['complexity_ratio']:.3f}")

def main():
    """Run all tests"""
    print("🧪 Experimental MLGrid - Art_Llama Integration Tests")
    print("=" * 80)
    
    # Run tests
    grid1 = test_art_llama_basic()
    grid2 = test_art_llama_evolution()
    grid3, grid4 = test_recursive_analysis()
    demonstrate_all_shifts()
    
    print("\n✅ All tests completed!")
    print("=" * 80)
    
    # Export final analysis
    print("\n📊 Exporting analysis data...")
    grid2.export_analysis("art_llama_evolution_test.json")
    
    print("🎯 Ready for research applications!")

if __name__ == "__main__":
    main()