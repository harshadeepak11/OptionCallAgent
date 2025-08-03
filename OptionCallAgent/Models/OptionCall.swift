//
//  OptionCall.swift
//  OptionCallAgent
//
//  Created by Harsha on 03/08/25.
//

import Foundation

struct OptionCall: Identifiable {
    let id = UUID()
    let type: String // Call or put
    let strikePrice: Double
    let expiry: String
    let reason: String
}
