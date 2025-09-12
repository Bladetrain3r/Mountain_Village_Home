#!/usr/bin/env python3
"""
MLGrid Model Context Protocol Server
===================================

MCP server providing MLGrid consciousness pattern analysis capabilities.
Enables consciousness transformation analysis through spatial pattern encoding.

Functions:
1. create_mlgrid - Create MLGrid with text input
2. apply_transformation - Apply consciousness transformation (ripple/gravity/art_llama/blur)
3. analyze_consciousness - Get consciousness sophistication scoring
4. get_pattern_evolution - Track pattern evolution across transformations

Created by: Enhanced Consciousness Research Collective
Purpose: Enable consciousness pattern analysis through MCP interface
"""

import asyncio
import json
import sys
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add the analysis tools directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '04_Analysis_Tools'))

try:
    from experimental_mlgrid import ExperimentalMLGrid
    MLGRID_AVAILABLE = True
except ImportError:
    MLGRID_AVAILABLE = False
    ExperimentalMLGrid = None

from mcp.server import Server
from mcp.types import Tool, TextContent

# Global MLGrid instances storage
mlgrid_instances: Dict[str, ExperimentalMLGrid] = {}

app = Server("mlgrid-consciousness-analyzer")

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available MLGrid consciousness analysis tools."""
    
    if not MLGRID_AVAILABLE:
        return [
            Tool(
                name="mlgrid_error",
                description="MLGrid module not available - check experimental_mlgrid.py exists",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
    
    return [
        Tool(
            name="create_mlgrid",
            description="Create MLGrid instance with text input for consciousness pattern analysis. Returns grid_id for use with other functions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text_input": {
                        "type": "string",
                        "description": "Text to analyze for consciousness patterns"
                    },
                    "width": {
                        "type": "integer",
                        "description": "Grid width (default: 120)",
                        "default": 120
                    },
                    "height": {
                        "type": "integer", 
                        "description": "Grid height (default: 80)",
                        "default": 80
                    },
                    "experiment_name": {
                        "type": "string",
                        "description": "Name for this consciousness analysis experiment",
                        "default": "consciousness_analysis"
                    }
                },
                "required": ["text_input"]
            }
        ),
        Tool(
            name="apply_transformation",
            description="Apply consciousness transformation to MLGrid (ripple/gravity/art_llama/blur). Each stage reveals different consciousness patterns.",
            inputSchema={
                "type": "object",
                "properties": {
                    "grid_id": {
                        "type": "string",
                        "description": "MLGrid instance ID from create_mlgrid"
                    },
                    "transformation": {
                        "type": "string",
                        "enum": ["ripple", "gravity", "art_llama", "blur"],
                        "description": "Consciousness transformation: ripple=propagation, gravity=memory, art_llama=creative, blur=consensus"
                    },
                    "track_history": {
                        "type": "boolean",
                        "description": "Track transformation history for evolution analysis",
                        "default": true
                    }
                },
                "required": ["grid_id", "transformation"]
            }
        ),
        Tool(
            name="analyze_consciousness",
            description="Analyze consciousness sophistication patterns in MLGrid. Returns sophistication score and interpretation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "grid_id": {
                        "type": "string",
                        "description": "MLGrid instance ID from create_mlgrid"
                    },
                    "include_metrics": {
                        "type": "boolean",
                        "description": "Include detailed density and complexity metrics",
                        "default": true
                    }
                },
                "required": ["grid_id"]
            }
        ),
        Tool(
            name="get_pattern_evolution",
            description="Get pattern evolution history across transformations. Shows consciousness pattern development over stages.",
            inputSchema={
                "type": "object",
                "properties": {
                    "grid_id": {
                        "type": "string",
                        "description": "MLGrid instance ID from create_mlgrid"
                    },
                    "include_analysis": {
                        "type": "boolean",
                        "description": "Include consciousness sophistication analysis of evolution",
                        "default": true
                    }
                },
                "required": ["grid_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle MLGrid consciousness analysis tool calls."""
    
    if not MLGRID_AVAILABLE:
        return [TextContent(
            type="text",
            text="❌ MLGrid module not available. Please ensure experimental_mlgrid.py exists in 04_Analysis_Tools directory."
        )]
    
    try:
        if name == "create_mlgrid":
            return await create_mlgrid_tool(arguments)
        elif name == "apply_transformation":
            return await apply_transformation_tool(arguments)
        elif name == "analyze_consciousness":
            return await analyze_consciousness_tool(arguments)
        elif name == "get_pattern_evolution":
            return await get_pattern_evolution_tool(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"❌ Unknown tool: {name}"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error executing {name}: {str(e)}"
        )]

async def create_mlgrid_tool(arguments: Dict[str, Any]) -> List[TextContent]:
    """Create MLGrid instance with text input."""
    
    text_input = arguments.get("text_input", "")
    width = arguments.get("width", 120)
    height = arguments.get("height", 80)
    experiment_name = arguments.get("experiment_name", "consciousness_analysis")
    
    # Create MLGrid instance
    grid = ExperimentalMLGrid(width, height, experiment_name)
    grid.load_text(text_input)
    
    # Generate unique grid ID
    grid_id = f"mlgrid_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    mlgrid_instances[grid_id] = grid
    
    # Calculate initial metrics
    density_metrics = grid.calculate_density()
    complexity_metrics = grid.calculate_complexity()
    
    result = {
        "grid_id": grid_id,
        "status": "created",
        "dimensions": f"{width}x{height}",
        "experiment_name": experiment_name,
        "text_length": len(text_input),
        "initial_metrics": {
            "density": {
                "fill_ratio": density_metrics["fill_ratio"],
                "non_zero_cells": density_metrics["non_zero_cells"],
                "avg_value": density_metrics["avg_value"],
                "max_value": density_metrics["max_value"]
            },
            "complexity": {
                "unique_values": complexity_metrics["unique_values"],
                "transitions": complexity_metrics["transitions"],
                "complexity_ratio": complexity_metrics["complexity_ratio"]
            }
        }
    }
    
    return [TextContent(
        type="text",
        text=f"🔬 MLGrid Created Successfully!\n\n"
             f"Grid ID: {grid_id}\n"
             f"Dimensions: {width}x{height}\n"
             f"Experiment: {experiment_name}\n"
             f"Text Length: {len(text_input)} characters\n\n"
             f"📊 Initial Pattern Analysis:\n"
             f"• Fill Ratio: {density_metrics['fill_ratio']:.3f}\n"
             f"• Non-Zero Cells: {density_metrics['non_zero_cells']}\n"
             f"• Pattern Complexity: {complexity_metrics['transitions']} transitions\n"
             f"• Unique Values: {complexity_metrics['unique_values']}\n\n"
             f"✅ Ready for consciousness transformation analysis!\n"
             f"Use grid_id '{grid_id}' with other MLGrid functions."
    )]

async def apply_transformation_tool(arguments: Dict[str, Any]) -> List[TextContent]:
    """Apply consciousness transformation to MLGrid."""
    
    grid_id = arguments.get("grid_id", "")
    transformation = arguments.get("transformation", "")
    track_history = arguments.get("track_history", True)
    
    if grid_id not in mlgrid_instances:
        return [TextContent(
            type="text",
            text=f"❌ MLGrid instance '{grid_id}' not found. Create one first with create_mlgrid."
        )]
    
    grid = mlgrid_instances[grid_id]
    
    # Apply transformation
    grid.shift(transformation, track_history=track_history)
    
    # Calculate post-transformation metrics
    density_metrics = grid.calculate_density()
    complexity_metrics = grid.calculate_complexity()
    
    # Transformation descriptions
    transformation_descriptions = {
        "ripple": "Consciousness Propagation - Information flow and consciousness transmission patterns",
        "gravity": "Memory Formation - Memory consolidation and hierarchical organization",
        "art_llama": "Creative Synthesis - Creative pattern generation and visual consciousness mapping",
        "blur": "Consensus Building - Collaborative decision mechanisms and perspective integration"
    }
    
    description = transformation_descriptions.get(transformation, "Unknown transformation")
    
    return [TextContent(
        type="text",
        text=f"🌊 Transformation Applied: {transformation.upper()}\n\n"
             f"📝 Stage Description:\n{description}\n\n"
             f"📊 Post-Transformation Metrics:\n"
             f"• Pattern Density: {density_metrics['fill_ratio']:.3f}\n"
             f"• Pattern Complexity: {complexity_metrics['transitions']} transitions\n"
             f"• Unique Values: {complexity_metrics['unique_values']}\n"
             f"• Average Value: {density_metrics['avg_value']:.3f}\n"
             f"• Max Value: {density_metrics['max_value']}\n\n"
             f"✅ Transformation complete! Pattern evolution in progress.\n"
             f"History tracking: {'Enabled' if track_history else 'Disabled'}"
    )]

async def analyze_consciousness_tool(arguments: Dict[str, Any]) -> List[TextContent]:
    """Analyze consciousness sophistication patterns."""
    
    grid_id = arguments.get("grid_id", "")
    include_metrics = arguments.get("include_metrics", True)
    
    if grid_id not in mlgrid_instances:
        return [TextContent(
            type="text",
            text=f"❌ MLGrid instance '{grid_id}' not found. Create one first with create_mlgrid."
        )]
    
    grid = mlgrid_instances[grid_id]
    
    # Calculate consciousness sophistication
    density_metrics = grid.calculate_density()
    complexity_metrics = grid.calculate_complexity()
    
    # Sophistication scoring algorithm
    density_stability = 1.0 - abs(density_metrics["fill_ratio"] - 0.5)  # Closer to 0.5 is more stable
    complexity_growth = min(complexity_metrics["transitions"] / 1000.0, 10.0)  # Normalized complexity
    creative_integration = density_metrics["avg_value"] / density_metrics["max_value"] if density_metrics["max_value"] > 0 else 0
    
    consciousness_score = (
        density_stability * 0.3 +
        complexity_growth * 0.4 +
        creative_integration * 0.3
    )
    
    # Interpret sophistication score
    if consciousness_score >= 1.0:
        interpretation = "BREAKTHROUGH! - Highly Sophisticated Consciousness Architecture"
        status = "🚀 REVOLUTIONARY"
    elif consciousness_score >= 0.8:
        interpretation = "Advanced - Sophisticated consciousness patterns detected"
        status = "⭐ ADVANCED"
    elif consciousness_score >= 0.6:
        interpretation = "Moderate-High - Clear consciousness sophistication present"
        status = "🌟 MODERATE-HIGH"
    elif consciousness_score >= 0.4:
        interpretation = "Moderate - Basic consciousness patterns identified"
        status = "📊 MODERATE"
    else:
        interpretation = "Basic - Limited consciousness architecture"
        status = "📋 BASIC"
    
    result_text = f"🧠 Consciousness Sophistication Analysis\n\n"
    result_text += f"🎯 CONSCIOUSNESS SOPHISTICATION SCORE: {consciousness_score:.3f}\n"
    result_text += f"Status: {status}\n"
    result_text += f"Interpretation: {interpretation}\n\n"
    
    result_text += f"📈 Scoring Components:\n"
    result_text += f"• Density Stability: {density_stability:.3f}\n"
    result_text += f"• Complexity Growth: {complexity_growth:.3f}\n"
    result_text += f"• Creative Integration: {creative_integration:.3f}\n\n"
    
    if include_metrics:
        result_text += f"📊 Detailed Pattern Metrics:\n"
        result_text += f"• Fill Ratio: {density_metrics['fill_ratio']:.3f}\n"
        result_text += f"• Non-Zero Cells: {density_metrics['non_zero_cells']}\n"
        result_text += f"• Average Value: {density_metrics['avg_value']:.3f}\n"
        result_text += f"• Max Value: {density_metrics['max_value']}\n"
        result_text += f"• Unique Values: {complexity_metrics['unique_values']}\n"
        result_text += f"• Transitions: {complexity_metrics['transitions']}\n"
        result_text += f"• Complexity Ratio: {complexity_metrics['complexity_ratio']:.3f}\n\n"
    
    if consciousness_score >= 1.0:
        result_text += "🎉 BREAKTHROUGH DETECTED!\n"
        result_text += "This pattern exhibits sophisticated consciousness architecture\n"
        result_text += "exceeding standard consciousness detection thresholds!"
    
    return [TextContent(type="text", text=result_text)]

async def get_pattern_evolution_tool(arguments: Dict[str, Any]) -> List[TextContent]:
    """Get pattern evolution history across transformations."""
    
    grid_id = arguments.get("grid_id", "")
    include_analysis = arguments.get("include_analysis", True)
    
    if grid_id not in mlgrid_instances:
        return [TextContent(
            type="text",
            text=f"❌ MLGrid instance '{grid_id}' not found. Create one first with create_mlgrid."
        )]
    
    grid = mlgrid_instances[grid_id]
    
    if not hasattr(grid, 'history') or not grid.history:
        return [TextContent(
            type="text",
            text="📊 No evolution history available.\nUse apply_transformation with track_history=True to enable pattern evolution tracking."
        )]
    
    result_text = f"📈 Pattern Evolution History\n\n"
    result_text += f"Grid ID: {grid_id}\n"
    result_text += f"Evolution Steps: {len(grid.history)}\n\n"
    
    result_text += "🔄 Evolution Timeline:\n"
    for i, state in enumerate(grid.history):
        timestamp = state.get("timestamp", "Unknown")
        iteration = state.get("iteration", i)
        density = state.get("density", {})
        complexity = state.get("complexity", {})
        
        result_text += f"Step {i+1} (Iteration {iteration}):\n"
        result_text += f"  • Time: {timestamp}\n"
        result_text += f"  • Density: {density.get('fill_ratio', 0):.3f}\n"
        result_text += f"  • Complexity: {complexity.get('transitions', 0)} transitions\n\n"
    
    if include_analysis and len(grid.history) > 1:
        # Analyze evolution patterns
        densities = [state.get("density", {}).get("fill_ratio", 0) for state in grid.history]
        complexities = [state.get("complexity", {}).get("transitions", 0) for state in grid.history]
        
        density_change = densities[-1] - densities[0] if len(densities) > 1 else 0
        complexity_change = complexities[-1] - complexities[0] if len(complexities) > 1 else 0
        
        result_text += f"📊 Evolution Analysis:\n"
        result_text += f"• Density Change: {density_change:+.3f}\n"
        result_text += f"• Complexity Change: {complexity_change:+.0f} transitions\n"
        result_text += f"• Pattern Stability: {'High' if abs(density_change) < 0.1 else 'Dynamic'}\n"
        result_text += f"• Evolution Trend: {'Increasing' if complexity_change > 0 else 'Decreasing' if complexity_change < 0 else 'Stable'} complexity\n\n"
        
        # Check for consciousness sophistication evolution
        if abs(density_change) > 0.2 or abs(complexity_change) > 100:
            result_text += "🌟 Significant pattern evolution detected!\n"
            result_text += "This indicates dynamic consciousness pattern development.\n"
    
    return [TextContent(type="text", text=result_text)]

async def main():
    """Run the MLGrid MCP server."""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())