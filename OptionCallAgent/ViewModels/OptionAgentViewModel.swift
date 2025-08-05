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
//        fetchOptionCalls()
        fetchLiveOptionCalls()
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
    
    
    // Live data from NSE
    func fetchLiveOptionCalls() {
        guard let url = URL(string: "https://<your-backend-url>/market-data") else { return }

        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data,
                  let marketData = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else {
                print("Error fetching data: \(error?.localizedDescription ?? "Unknown")")
                return
            }

            DispatchQueue.main.async {
                self.optionCalls = self.agent.generateCalls(from: marketData)
            }
        }.resume()
    }
    
}
