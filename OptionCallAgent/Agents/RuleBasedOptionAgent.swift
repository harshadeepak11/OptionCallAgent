//
//  RuleBasedOptionAgent.swift
//  OptionCallAgent
//
//  Created by Harsha on 03/08/25.
//

import Foundation

class RuleBasedOptionAgent {
    
    func generateCalls(from marketData: [String:Any]) -> [OptionCall] {
        guard let nifty = marketData["nifty"] as? Double,
              let trend = marketData["trend"] as? String,
              let dma = marketData["50dma"] as? Double,
              let resistance = marketData["resistance"] as? Double,
              let support = marketData["support"] as? Double,
              let iv = marketData["iv"] as? Double else {
            return []
        }
        
        var calls: [OptionCall] = []
        if trend == "Bullish" {
            let call = OptionCall(
                type: .call,
                strikePrice: nifty + 100,
                expiry: DateFormatter().date(from: "08-Aug-2025") ?? Date(),
                reason: "Nifty is trending up. Buy near the money CALL option.")
            calls.append(call)
        }
        if trend == "Bearish" {
            let put = OptionCall(
                type: .put,
                strikePrice: nifty + 100,
                expiry: DateFormatter().date(from: "08-Aug-2025") ?? Date(),
                reason: "Nifty is trending down. Buy near the money PUT option.")
            calls.append(put)
        }
        if iv > 15 {
                calls.append(OptionCall(
                    type: .sell,
                    strikePrice: nifty,
                    expiry: DateFormatter().date(from: "08-Aug-2025") ?? Date(),
                    reason: "High implied volatility. Consider selling options (advanced strategy)."
                ))
            }
        return calls
    }
}
