import Alamofire
import UIKit
import HealthKit

let healthKitStore: HKHealthStore = HKHealthStore()

class DashboardViewController: UIViewController {
    
    @IBOutlet weak var age: UILabel!
    @IBOutlet weak var heart: UILabel!
    
    @IBAction func updateButton(_ sender: Any) {
        let (age, bloodType) = readData()
        self.age.text = "\(String(age!))"
        
        //Reading BPM
        self.readMostRecentSample()
    }
    
    @IBAction func authorize(_ sender: Any) {
        self.authorizeHealthKitInApp()
    }
    
    func readData() -> (age:Int?, bloodType:HKBloodTypeObject?) {
        
        var age:Int?
        var bloodType:HKBloodTypeObject?
        
        //Reading the date of birth
        do {
            let birthday = try healthKitStore.dateOfBirthComponents()
            let currentYear = Calendar.current.component(.year, from: Date())
            age = currentYear - birthday.year!
        } catch {}
        
        //Reading the blood type
        do {
            bloodType = try healthKitStore.bloodType()
        } catch {}
        
        return (age, bloodType)
        
    }
    
    func readMostRecentSample() {
        
        let BPM = HKSampleType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate)
        
        let query = HKSampleQuery(sampleType: BPM!, predicate: nil, limit: HKObjectQueryNoLimit, sortDescriptors: nil) { (query, results, error) in
            if let result = results?.last as? HKQuantitySample {
                print("BPM = \(result.quantity)")
                DispatchQueue.main.async(execute: { () -> Void in
                    self.heart.text = "\(result.quantity)"
                })
            }
        }
    }
    
    func authorizeHealthKitInApp() {
        
        let healthKitTypeToRead: Set<HKObjectType> = [
            HKObjectType.characteristicType(forIdentifier: HKCharacteristicTypeIdentifier.dateOfBirth)!,
            HKObjectType.characteristicType(forIdentifier: HKCharacteristicTypeIdentifier.bloodType)!,
            HKObjectType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate)!,
        ]
        
        let healthKitTypeToWrite: Set<HKSampleType> = []
        
        if !HKHealthStore.isHealthDataAvailable() {
            print("Data not available")
            return
        }
        
        healthKitStore.requestAuthorization(toShare: healthKitTypeToWrite, read: healthKitTypeToRead) { (success, error) -> Void in
            print("Read & Write authorization acquired!")
        }
        
    }
    
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
