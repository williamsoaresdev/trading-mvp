using TradingExecutor.Domain.Interfaces;
using TradingExecutor.Domain.Models;

namespace TradingExecutor.Application.Services;

/// <summary>
/// Application service that orchestrates the trading execution process.
/// Follows Single Responsibility Principle - coordinates between different services.
/// </summary>
public class TradingExecutionService
{
    private readonly IWebSocketClient _webSocketClient;
    private readonly IOrderExecutor _orderExecutor;
    private readonly IRiskManager _riskManager;
    private readonly ITradingLogger _logger;
    private readonly IConfigurationProvider _config;
    
    private readonly CancellationTokenSource _cancellationTokenSource = new();
    private bool _isRunning = false;

    public TradingExecutionService(
        IWebSocketClient webSocketClient,
        IOrderExecutor orderExecutor,
        IRiskManager riskManager,
        ITradingLogger logger,
        IConfigurationProvider config)
    {
        _webSocketClient = webSocketClient ?? throw new ArgumentNullException(nameof(webSocketClient));
        _orderExecutor = orderExecutor ?? throw new ArgumentNullException(nameof(orderExecutor));
        _riskManager = riskManager ?? throw new ArgumentNullException(nameof(riskManager));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _config = config ?? throw new ArgumentNullException(nameof(config));
        
        // Subscribe to events
        _webSocketClient.TradingDecisionReceived += OnTradingDecisionReceived;
        _webSocketClient.ConnectionStatusChanged += OnConnectionStatusChanged;
    }

    /// <summary>
    /// Start the trading execution service.
    /// </summary>
    public async Task StartAsync()
    {
        if (_isRunning)
        {
            await _logger.LogSystemEventAsync("WARNING", "Trading service is already running");
            return;
        }

        try
        {
            await _logger.LogSystemEventAsync("INFO", "🚀 Starting Real-Time Trading Executor");
            
            _isRunning = true;
            
            // Connect to WebSocket
            var wsUri = _config.GetWebSocketUri();
            await _webSocketClient.ConnectAsync(wsUri, _cancellationTokenSource.Token);
            
            // Start listening for messages
            await _webSocketClient.StartListeningAsync(_cancellationTokenSource.Token);
        }
        catch (Exception ex)
        {
            _isRunning = false;
            await _logger.LogSystemEventAsync("ERROR", "Failed to start trading service", ex);
            throw;
        }
    }

    /// <summary>
    /// Stop the trading execution service.
    /// </summary>
    public async Task StopAsync()
    {
        if (!_isRunning)
        {
            return;
        }

        try
        {
            await _logger.LogSystemEventAsync("INFO", "🛑 Stopping trading executor");
            
            _cancellationTokenSource.Cancel();
            _isRunning = false;
            
            await _webSocketClient.DisconnectAsync();
            
            await _logger.LogSystemEventAsync("INFO", "✅ Trading executor stopped successfully");
        }
        catch (Exception ex)
        {
            await _logger.LogSystemEventAsync("ERROR", "Error during shutdown", ex);
        }
    }

    /// <summary>
    /// Handle incoming trading decisions.
    /// </summary>
    private async void OnTradingDecisionReceived(object? sender, TradingDecision decision)
    {
        try
        {
            await _logger.LogDecisionReceivedAsync(decision);
            
            // 1. Validate decision
            if (!decision.IsValidForExecution)
            {
                await _logger.LogSystemEventAsync("WARNING", $"Invalid decision received: {decision.DecisionId}");
                return;
            }
            
            // 2. Apply risk management
            var managedDecision = await _riskManager.ApplyRiskManagementAsync(decision);
            
            if (!_riskManager.IsDecisionValid(managedDecision))
            {
                await _logger.LogSystemEventAsync("INFO", $"Decision rejected by risk management: {decision.DecisionId}");
                return;
            }
            
            // 3. Execute the order
            if (!managedDecision.Prediction.IsFlatSignal)
            {
                var executionResult = await _orderExecutor.ExecuteOrderAsync(managedDecision, _cancellationTokenSource.Token);
                await _logger.LogOrderExecutionAsync(executionResult);
                
                if (!executionResult.IsSuccessful)
                {
                    await _logger.LogSystemEventAsync("ERROR", $"Order execution failed: {executionResult.ErrorMessage}");
                }
            }
            else
            {
                await _logger.LogSystemEventAsync("INFO", "FLAT signal - no execution required");
            }
        }
        catch (Exception ex)
        {
            await _logger.LogSystemEventAsync("ERROR", $"Error processing trading decision: {decision.DecisionId}", ex);
        }
    }

    /// <summary>
    /// Handle connection status changes.
    /// </summary>
    private async void OnConnectionStatusChanged(object? sender, bool isConnected)
    {
        var status = isConnected ? "connected" : "disconnected";
        await _logger.LogSystemEventAsync("INFO", $"WebSocket {status}");
    }

    /// <summary>
    /// Dispose resources.
    /// </summary>
    public void Dispose()
    {
        _cancellationTokenSource?.Cancel();
        _cancellationTokenSource?.Dispose();
        _webSocketClient?.Dispose();
    }
}