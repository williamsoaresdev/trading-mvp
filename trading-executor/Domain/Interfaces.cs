using TradingExecutor.Domain.Models;

namespace TradingExecutor.Domain.Interfaces;

/// <summary>
/// Interface for WebSocket communication with trading services.
/// Follows Interface Segregation Principle - only WebSocket-related methods.
/// </summary>
public interface IWebSocketClient : IDisposable
{
    /// <summary>
    /// Event fired when a new trading decision is received.
    /// </summary>
    event EventHandler<TradingDecision> TradingDecisionReceived;
    
    /// <summary>
    /// Event fired when connection status changes.
    /// </summary>
    event EventHandler<bool> ConnectionStatusChanged;
    
    /// <summary>
    /// Connect to the WebSocket endpoint.
    /// </summary>
    Task ConnectAsync(string uri, CancellationToken cancellationToken = default);
    
    /// <summary>
    /// Start listening for messages.
    /// </summary>
    Task StartListeningAsync(CancellationToken cancellationToken = default);
    
    /// <summary>
    /// Send a message through the WebSocket.
    /// </summary>
    Task SendMessageAsync(string message, CancellationToken cancellationToken = default);
    
    /// <summary>
    /// Check if WebSocket is currently connected.
    /// </summary>
    bool IsConnected { get; }
    
    /// <summary>
    /// Disconnect from WebSocket.
    /// </summary>
    Task DisconnectAsync();
}

/// <summary>
/// Interface for order execution.
/// Single Responsibility: only handles order execution logic.
/// </summary>
public interface IOrderExecutor
{
    /// <summary>
    /// Execute a trading order based on the decision.
    /// </summary>
    Task<OrderExecutionResult> ExecuteOrderAsync(TradingDecision decision, CancellationToken cancellationToken = default);
}

/// <summary>
/// Interface for risk management.
/// Single Responsibility: only handles risk-related calculations and validations.
/// </summary>
public interface IRiskManager
{
    /// <summary>
    /// Apply risk management rules to a trading decision.
    /// </summary>
    Task<TradingDecision> ApplyRiskManagementAsync(TradingDecision decision);
    
    /// <summary>
    /// Validate if a decision meets risk criteria.
    /// </summary>
    bool IsDecisionValid(TradingDecision decision);
    
    /// <summary>
    /// Calculate adjusted position size based on risk parameters.
    /// </summary>
    double CalculateAdjustedPositionSize(double originalSize, double riskScore);
}

/// <summary>
/// Interface for logging trading activities.
/// Single Responsibility: handles all logging concerns.
/// </summary>
public interface ITradingLogger
{
    /// <summary>
    /// Log a trading decision received.
    /// </summary>
    Task LogDecisionReceivedAsync(TradingDecision decision);
    
    /// <summary>
    /// Log order execution result.
    /// </summary>
    Task LogOrderExecutionAsync(OrderExecutionResult result);
    
    /// <summary>
    /// Log system events (connections, errors, etc.).
    /// </summary>
    Task LogSystemEventAsync(string level, string message, Exception? exception = null);
    
    /// <summary>
    /// Log risk management actions.
    /// </summary>
    Task LogRiskManagementAsync(string action, TradingDecision originalDecision, TradingDecision adjustedDecision);
}

/// <summary>
/// Interface for configuration management.
/// Single Responsibility: provides configuration values.
/// </summary>
public interface IConfigurationProvider
{
    /// <summary>
    /// Get WebSocket connection URI.
    /// </summary>
    string GetWebSocketUri();
    
    /// <summary>
    /// Get risk management settings.
    /// </summary>
    RiskManagementConfig GetRiskManagementConfig();
    
    /// <summary>
    /// Get trading execution settings.
    /// </summary>
    TradingExecutionConfig GetTradingExecutionConfig();
}

/// <summary>
/// Configuration for risk management parameters.
/// </summary>
public sealed record RiskManagementConfig
{
    public double MaxPositionSize { get; init; } = 0.02; // 2%
    public double MinConfidenceThreshold { get; init; } = 0.6; // 60%
    public double MaxDailyLoss { get; init; } = 0.04; // 4%
    public bool EnableRiskManagement { get; init; } = true;
}

/// <summary>
/// Configuration for trading execution parameters.
/// </summary>
public sealed record TradingExecutionConfig
{
    public bool EnableRealTrading { get; init; } = false; // Mock by default
    public string ExchangeApiKey { get; init; } = string.Empty;
    public string ExchangeSecretKey { get; init; } = string.Empty;
    public TimeSpan OrderTimeout { get; init; } = TimeSpan.FromSeconds(30);
    public int MaxRetryAttempts { get; init; } = 3;
}