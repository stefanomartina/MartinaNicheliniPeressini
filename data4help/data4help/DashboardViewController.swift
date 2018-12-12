import Alamofire
import UIKit
import HealthKit

let healthKitStore: HKHealthStore = HKHealthStore()

class DashboardViewController: UIViewController {
    
    @IBAction func updateAndUpload(_ sender: UIButton) {
        var returned: [HKQuantitySample] = HealthKitManager.getLastHeartBeat()
        
        if returned.count == 0 {
            let message = "No new data were found"
            let alert = UIAlertController(title: "Attention", message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
            self.present(alert, animated: true)
        } else {
            let message = String(format: "%x%@", returned.count, " elements were found")
            let alert = UIAlertController(title: "Success", message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
            self.present(alert, animated: true)
        }

    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
    
}
