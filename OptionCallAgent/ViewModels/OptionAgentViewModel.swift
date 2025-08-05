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
        
        let decoder = JSONDecoder()
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss"
        decoder.dateDecodingStrategy = .formatted(formatter)
        
        guard let url = URL(string: "https://optioncallagent-1.onrender.com/option-calls") else {
                print("Invalid URL")
                return
            }

//            decoder.dateDecodingStrategy = .iso8601

            URLSession.shared.dataTask(with: url) { data, response, error in
                if let data = data {
                    do {
                        let optionCalls = try decoder.decode([OptionCall].self, from: data)
                                DispatchQueue.main.async {
                                    self.optionCalls = optionCalls
                                }
                    } catch {
                        if let jsonString = String(data: data, encoding: .utf8) {
                            print("🔎 JSON Response:\n\(jsonString)")
                        }
                        print("Decoding error:", error)
                    }
                } else if let error = error {
                    print("Network error:", error)
                }
            }.resume()
    }
    
}
