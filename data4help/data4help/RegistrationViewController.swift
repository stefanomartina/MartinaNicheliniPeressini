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
    
    @IBOutlet weak var textFieldGender: UITextField!
    @IBOutlet var genderPicker: UIPickerView! = UIPickerView()
    
    @IBOutlet weak var textFieldFiscalCode: UITextField!
    
    @IBOutlet weak var labelMessage: UILabel!
    
    @IBAction func buttonRegister(_ sender: UIButton) {
        let parameters : Parameters=[
            "firstname":textFieldFirstName.text!,
            "lastname":textFieldLastName.text!,
            "username":textFieldUsername.text!,
            "password":textFieldPassword.text!
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
    
    
    
    
    
    
    
    
    
    func numberOfComponentsInPickerView(pickerView: UIPickerView!) -> Int{
        return 1
    }
    
    func pickerView(pickerView: UIPickerView!, numberOfRowsInComponent component: Int) -> Int{
        return GENDERS.count
    }
    
    func pickerView(pickerView: UIPickerView!, titleForRow row: Int, forComponent component: Int) -> String! {
        return GENDERS[row]
    }
    
    func pickerView(pickerView: UIPickerView!, didSelectRow row: Int, inComponent component: Int)
    {
        textFieldGender.text = GENDERS[row]
        genderPicker.isHidden = true;
    }
    
    func textFieldShouldBeginEditing(textField: UITextField) -> Bool {
        genderPicker.isHidden = false
        return false
    }
    
    
    
    
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
//        genderPicker.isHidden = true
    }
    
}
