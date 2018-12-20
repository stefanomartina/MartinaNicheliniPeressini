//
//  SubscriptionTableViewCell.swift
//  data4help
//
//  Created by Alessandro Nichelini on 20/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit

class SubscriptionTableViewCell: UITableViewCell {

    @IBOutlet weak var requesterNameLabel: UILabel!
    @IBOutlet weak var actualStatusLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
