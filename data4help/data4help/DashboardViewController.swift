import Alamofire
import UIKit
import HealthKit

class DashboardViewController: UIViewController {

    @IBAction func updateAndUpload(_ sender: UIButton) {
        var returned: [Double] = []
        if returned.count == 0 {
            let message = "No new data found"
            let alert = UIAlertController(title: "Attention", message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
            self.present(alert, animated: true)
        }
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
    
}
