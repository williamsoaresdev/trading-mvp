using System.Text.Json;

namespace TradingExecutor.Domain.Models;

/// <summary>
/// Value object representing a trading decision received from the ML service.
/// Immutable and contains all data needed for trading execution.
/// </summary>
public sealed record TradingDecision
{
    public required string DecisionId { get; init; }
    public required string Timestamp { get; init; }
    public required string Symbol { get; init; }
    public required TradingPrediction Prediction { get; init; }
    
    public bool IsValidForExecution => 
        !string.IsNullOrEmpty(DecisionId) && 
        !string.IsNullOrEmpty(Symbol) && 
        Prediction != null;
}

/// <summary>
/// Value object containing prediction data from ML model.
/// </summary>
public sealed record TradingPrediction
{
    public required string Action { get; init; }
    public required double ProbabilityBuy { get; init; }
    public required double ProbabilitySell { get; init; }
    public required decimal CurrentPrice { get; init; }
    public required double PositionFraction { get; init; }
    public required double AtrPercentage { get; init; }
    
    public bool IsBuySignal => Action.Equals("BUY", StringComparison.OrdinalIgnoreCase);
    public bool IsSellSignal => Action.Equals("SELL", StringComparison.OrdinalIgnoreCase);
    public bool IsFlatSignal => Action.Equals("FLAT", StringComparison.OrdinalIgnoreCase);
    
    public double MaxProbability => Math.Max(ProbabilityBuy, ProbabilitySell);
    public bool MeetsConfidenceThreshold(double threshold) => MaxProbability >= threshold;
}

/// <summary>
/// Value object representing WebSocket message structure.
/// </summary>
public sealed record WebSocketMessage
{
    public required string Type { get; init; }
    public required JsonElement Data { get; init; }
}

/// <summary>
/// Value object for order execution results.
/// </summary>
public sealed record OrderExecutionResult
{
    public required string OrderId { get; init; }
    public required string Symbol { get; init; }
    public required string Action { get; init; }
    public required decimal ExecutionPrice { get; init; }
    public required double PositionSize { get; init; }
    public required DateTime ExecutionTime { get; init; }
    public required string Status { get; init; }
    public string? ErrorMessage { get; init; }
    
    public bool IsSuccessful => Status.Equals("FILLED", StringComparison.OrdinalIgnoreCase);
}