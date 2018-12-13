import Alamofire
import UIKit
import HealthKit
import SwiftyJSON

let healthKitStore: HKHealthStore = HKHealthStore()

class DashboardViewController: UIViewController {
    
    @IBAction func updateAndUpload(_ sender: UIButton) {
        updateData()
    }
    
    func updateData(){
        let queryReturned: [HKQuantitySample] = HealthKitManager.getLastHeartBeat()
        
        if queryReturned.count == 0 {
            let message = "No new data were found"
            let alert = UIAlertController(title: "Attention", message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
            self.present(alert, animated: true)
        }
        else {
            let message = String(format: "%x%@", queryReturned.count, " elements were found")
            let alert = UIAlertController(title: "Success", message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
            self.present(alert, animated: true)
        }
        
        DispatchQueue.main.async {
            HTTPManager.sendHeartData(data: queryReturned)
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        updateData()
        // Do any additional setup after loading the view.
    }
    
}
