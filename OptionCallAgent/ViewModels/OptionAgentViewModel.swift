//
//  OptionAgentViewModel.swift
//  OptionCallAgent
//
//  Created by Harsha on 03/08/25.
//

import Foundation

class OptionAgentViewModel: ObservableObject {
    @Published var optionCalls: [OptionCall] = []
    
    private let agent = RuleBasedOptionAgent()
    
    init() {
        fetchOptionCalls()
    }
    
    func fetchOptionCalls() {
        let mockData: [String: Any] = [
            "nifty": 25000.0,
            "trend": "Bearish",
            "50dma":21900.0,
            "resistance": 22300.0,  // chart resistance
            "support": 22100.0,     // chart support
            "iv": 17.5              // Implied Volatility
        ]
        
        optionCalls = agent.generateCalls(from: mockData)
    }
    
}
