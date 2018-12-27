//
//  LocationDataTableViewCell.swift
//  data4help
//
//  Created by Alessandro Nichelini on 27/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit

class LocationDataTableViewCell: UITableViewCell {

    @IBOutlet weak var coordinatesLabel: UILabel!
    @IBOutlet weak var timestampLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
