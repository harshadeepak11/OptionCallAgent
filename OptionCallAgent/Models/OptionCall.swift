//
//  OptionCall.swift
//  OptionCallAgent
//
//  Created by Harsha on 03/08/25.
//

import Foundation

enum OptionType: String {
    case call = "CALL"
    case put = "PUT"
    case sell = "SELL"
}

struct OptionCall: Identifiable, Decodable {
    let id = UUID()
    let type: String
    let strikePrice: Double
    let expiry: Date
    let reason: String
}
