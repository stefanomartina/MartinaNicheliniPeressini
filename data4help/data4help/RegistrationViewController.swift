import Alamofire
import UIKit

class RegistrationViewController: UIViewController {
    
    let URL_USER_REGISTER = Global.getUserURL() + Global.REGISTER_METHOD
    let GENDERS = ["M", "F"]
    
    @IBOutlet weak var textFieldFirstName: UITextField!
    @IBOutlet weak var textFieldLastName: UITextField!
    @IBOutlet weak var textFieldUsername: UITextField!
    @IBOutlet weak var textFieldPassword: UITextField!
    @IBOutlet weak var textFieldBirthPlace: UITextField!
    
    @IBOutlet weak var textFieldBirthDate: UITextField!
    @IBOutlet weak var datePicker: UIDatePicker!
    
    @IBOutlet weak var textFieldGender: UITextField!
    
    @IBOutlet weak var textFieldFiscalCode: UITextField!
    
    @IBOutlet weak var labelMessage: UILabel!
    
    @IBAction func buttonRegister(_ sender: UIButton) {
        let parameters : Parameters=[
            "firstname":textFieldFirstName.text!,
            "lastname":textFieldLastName.text!,
            "username":textFieldUsername.text!,
            "password":textFieldPassword.text!,
            "birthdate": textFieldBirthDate.text!,
            "birthplace": textFieldBirthPlace.text!,
            "gender": textFieldBirthPlace.text!,
            "fiscalcode": textFieldFiscalCode.text!
        ]
        
        Alamofire.request(URL_USER_REGISTER, method: .post, parameters: parameters, encoding: JSONEncoding.default)
            .responseJSON {
                response in
                if let status = response.result.value {
                    let JSON = status as! NSDictionary;
                    let appo = JSON["Response"]!;
                    print(appo)
                }
        }
    }

     /////////////////////////////////////////////////// DATE KEEPER
    
    @IBAction func dp(_ sender: UITextField) {
        let datePickerView = UIDatePicker()
        datePickerView.datePickerMode = .date
        sender.inputView = datePickerView
        datePickerView.addTarget(self, action: #selector(handleDatePicker(sender:)), for: .valueChanged)
    }
    
    @objc func handleDatePicker(sender: UIDatePicker) {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "dd MMM yyyy"
        textFieldBirthDate.text = dateFormatter.string(from: sender.date)
    }
    
    
    /////////////////////////////////////////////////// OVERRIDE DEFAULT VIEW FUNCTION
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.hideKeyboardWhenTappedAround()
    }
    
}
