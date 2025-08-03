//
//  HomeView.swift
//  OptionCallAgent
//
//  Created by Harsha on 03/08/25.
//

import SwiftUI

struct HomeView: View {
    
    @StateObject private var viewModel = OptionAgentViewModel()
    
    var body: some View {
        NavigationView {
            List(viewModel.optionCalls) { call in
                VStack(alignment: .leading, spacing: 5) {
                    Text("\(call.type) Option @ \(call.strikePrice, specifier: "%.0f")")
                                            .font(.headline)
                    Text("Expiry: \(call.expiry)")
                                            .font(.subheadline)
                                        Text("Reason: \(call.reason)")
                                            .font(.caption)
                                            .foregroundColor(.gray)
                }
                .padding(.vertical, 4)
            }
            .navigationTitle("Option Calls")
        }
    }
}

#Preview {
    HomeView()
}


