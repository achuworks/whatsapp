import os
import re

# List of student names as target names
student_names = [
    'Suthanya A', 'Dinesh Pranav K S', 'Tharun Adith V', 'Keerthana H', 'M Dhayanithi',
    'Rishi S', 'Pranav R', 'Ananthu AS', 'Shakthi Srinithi S', 'Akhil Joseph LG',
    'Logeshwari S', 'Sasmitha Krishnamoorthy', 'Santhiya E', 'Siva Swetha SCK',
    'Harish J', 'Dharani Daran G', 'Rithika M', 'Bharath Kumar MS', 'Kisore P',
    'Ranjana S', 'Varun Rohit', 'R Sajith', 'Raguram M', 'Ranjith S', 'Geethanjali GP',
    'Arun A', 'Sharvitha GV', 'Hari Priya Gatla', 'Agalya P', 'Pranesh I', 'Harish S',
    'Karthik R', 'Arun Kumar M', 'A J Divyaprakash', 'Dinesh P', 'Kiran P', 'Logesh B',
    'Dhana Varshini S', 'Priyanka R', 'Niviya S V', 'Bomathi S', 'Dhanush G',
    'Jeevasathya B', 'Sanjay Srinivas T', 'Karthikraja R', 'Arjun Sarkesh S',
    'Varalakshmi R', 'Prahathi S', 'Aparna A', 'Shivasurya J', 'Meera S S',
    'M Sandhiya', 'Sarvesh J A', 'K Jhothi Prakash', 'Dikshinth', 'A Anitha',
    'Tarun Velumani', 'Nandhini R', 'Boobalan S A', 'Pandiyarajan S', 'Bavana E',
    'Thangaraj P', 'Sugumaran S', 'S Naveenkumar', 'Shivani G', 'Divya Ranjani R',
    'Mythili G', 'Netra R', 'Preethi S', 'Abirami P', 'Prashanth S H', 'Madhumitha',
    'Kavipriya A', 'Punitha Princilla S', 'Haripriya P', 'R Maaya Shri', 'Madhan G',
    'Aswin S', 'Ranjan P', 'Harish P', 'Lavanya S', 'Shanjay K', 'Subhiksha S',
    'Prakash K', 'Deepa G', 'Preethica B', 'B Logapriyadharshini', 'Lakshana R',
    'Nandhika Sri S', 'Jayarajan S', 'Deepsikasri R G', 'Deepikadevi M', 'Prabin C S',
    'Nandhini R', 'Kumaraguru G', 'Manoj M', 'Sylvia A', 'Muhammad Yunus S',
    'Kanishkanth M S', 'Kousik K Y', 'Ramya S', 'Sneha Sree V', 'Vibin R',
    'Sowdhanyaa M', 'Paruthiya R', 'Calista Stephanie A', 'Nandhini G',
    'Danush Karthic J', 'Vikas B', 'Ahalya R', 'Padmapriya S', 'Rakul', 'Tanisshq M',
    'Mahalakshmi', 'Sumetha K', 'Sanjay R', 'Yogalakshmi R', 'Rashwanth E M',
    'Kousalya A', 'Anugraha J', 'Koodalarasu M', 'Ramya M', 'Harini P', 'Harshini A',
    'T Dhanashrri', 'Nitin B', 'Lavanya S', 'Yogeshwaran S', 'Nandakumar S G',
    'Arul Immanuel T', 'Balamurugan A', 'Lavanya N', 'V P Aravinthan', 'Vijay',
    'Santhiya R', 'Kokula Krishnan S', 'Gokulan V', 'Harshak S', 'Harshavardhini V S',
    'Bharathi S', 'Prasanna B', 'Ramchandh S', 'Sabari Vasan C S', 'Monish R',
    'Rupesh D', 'Deepak Raj D', 'Vignesh Kumar S', 'Nancy A', 'Amritha S',
    'I Sahira Fathima', 'Janani Aiswarya M', 'Varshini A', 'N Kanika',
    'Mohammed Samiel S', 'Vishal K', 'Yasaswini R', 'Prabhahar B', 'Faizal Ahamed A',
    'Rupa R', 'Renisha Gnanajesus', 'Nithyasree P', 'Gowinya S', 'David Meshach P',
    'Kowsika M', 'Guhapriya Ramesh', 'Soundarya S', 'Kanish R T', 'Preethika Periyasamy',
    'Hari Shankar P', 'Menaka R', 'Darshana S', 'Gayathri H', 'Dharanidhar A',
    'Sivapriya S', 'Sanjai Kumar S', 'Sushmitha M', 'Pooja P', 'Jenish S',
    'Dhivyadharshini V', 'N Nirmal S', 'Mohana Priyan K', 'Merrin Olivia N',
    'Vyshali S', 'Saniya MV', 'Kavin KGV', 'Hemalatha R', 'Haji Mohamed A',
    'Lakshmipriya N', 'Shri Varsha S', 'Nikitha Agnes A', 'Sharadha Sree J S',
    'Ashima Fathima', 'Shanmugapriya A', 'Marudhuvigneshwar', 'Jones Felix CK',
    'Koushika CP', 'Akshay', 'Haridha Mahalingam', 'Kiruthiga KM', 'Vidhya V',
    'Shyam SG', 'Rooba K', 'Tamilarasi K S', 'Durga Devi S', 'Srimathi Sangamithira S K',
    'Abdul Kareem E', 'Indhu Priyan', 'Arjun M', 'Krishnan SA', 'B Sasmila',
    'Varshini P', 'Revathi A', 'Dinesh J', 'J Padmapriya', 'Narmatha S', 'K S Revanth',
    'Hemarekha S', 'Udhayasree R', 'Kavipriya S', 'Pavithra K', 'Sruthika S',
    'Brindhaa S', 'Sobana S', 'Lavanya', 'Sakthishree D', 'Kavya M', 'Kiruthika S',
    'Jai Aditya T', 'Gokul P', 'Pratheep D', 'S ThiruMurugan', 'Kavieshwara M',
    'Tharun R M', 'Dhayalini P', 'Darshan R A', 'Shanmathi S', 'Monica S',
    'Winston Churchil S', 'Udhaya R', 'G Ajaikumar', 'Arthi S', 'M R Sriram',
    'Arasu Pandian N', 'Anand K', 'Nithikkannan J S', 'Harini KS', 'Suman S',
    'K R Nitin', 'Sankamesh VS', 'M Manova', 'Arputha Siva Sree V J', 'Vaishnavi Priya K',
    'Sanjeev G H', 'Raghul Vasun V T', 'Nithish N', 'Anjana Sri S', 'Kabhilesh Mk',
    'Mohan Kumar M', 'Dr S Rajalaxmi', 'Dharshini V', 'Deepika A', 'Bhoomash A K',
    'Karuppayammal S', 'Yaswanth S', 'Gowsalya G', 'V Mekavarshine', 'Prathakshana VA',
    'Jai Shree S', 'Swetha S', 'Ramprasath S', 'Dhanusri M', 'Dhaheera M',
    'Nitharsan S G', 'Shakthi Priya T', 'Nesiga A', 'Jayanthi', 'Harish K',
    'Mouli B', 'Yogesh S', 'Krithika S', 'Sharadha Sree J S', 'Sanmathi Priya K S',
    'Ponni M', 'Kanmani Pachagoundan', 'Sujithkumar S', 'Sangeetha M',
    'Mithun Kumar Nagarajan', 'Sriram K', 'Bagath', 'Krishna K', 'Gowtham N',
    'Sridhar A', 'Asvithaa K', 'Kavya M', 'Priyadharshini S', 'Santhosh',
    'Mahendran G R', 'Sowmiya T', 'Senthamizhselvam', 'Sanjeev GH', 'V Hariharen',
    'Sri Vatsan P', 'Dharshini M', 'Sanjai Gunawanth R', 'Retiha C', 'Sudharsana B',
    'Aasima M H', 'Nikitha Singanallur Babu', 'Megaa J', 'Sakthisri R', 'Kumaravel S',
    'Dhanushsree C', 'Gowrish T', 'Madhumitha J', 'Senthamizh M', 'Pavithra B',
    'Madumitha G', 'Preethi H', 'Madhumitraa P', 'Samiksha K K', 'V R Dheepan',
    'Soorya Velaa P', 'Mohana Prabhu G', 'Swetha K', 'Niranjan', 'Brinda P',
    'Thejasvie P Gopinath', 'Karthikha Shree S M', 'Ifa S A', 'Jai Abinav T',
    'Keerthikumar R', 'Kowsalya P', 'Vishwanathan N', 'Ramalingam M', 'Logupriya A',
    'Mohamed Jaim', 'Thaneesha R', 'Pratharshan A T', 'Abishek V', 'Vejayakant T K',
    'Vickneshwaran K', 'Nikhitha KV', 'Durga VB', 'Harini Sri V', 'Vishnupriya K',
    'N Krishna', 'Sarmitha S', 'Shubanithi Chakkaravarthi', 'Tharani M', 'Sajitha S',
    'Soundarya S', 'Siddharth M', 'Srikarthika M', 'M Dharshini', 'Pavilan S',
    'Siddharthan K', 'Geo Jeevan Raj C', 'Siva Sakthii U S', 'Manimaran M',
    'G Prasanna', 'Mithrajith K S', 'Bharath G', 'Nivetha A', 'Neha S', 'Gowtham TJ',
    'Daruniga M V', 'Muthulakshmi M', 'Hemachandran S B', 'Bharath K A', 'Kalimuthu',
    'Prakash K', 'Gopika P', 'Monish V', 'Snehala A', 'Aswathi R', 'Gopika A S',
    'Velayutham S', 'Bharath G', 'Harinivas M', 'Kirthikaa M K', 'Anushri M',
    'Krishnan T', 'Sweatha J', 'Hariharan P R', 'Dharshanashri G', 'Gokul Sriram S',
    'Jaya Suriya K', 'Deepak T', 'Jagadees', 'Alfie A', 'Ashika V U',
    'M Subbash Chandra Bose', 'Surya S', 'Selvakumar K', 'Thilagaraj', 'Karthik',
    'Dhinakaran', 'Dinesh Kumar R', 'Vishnu AP', 'Sajith J', 'Rithik P A',
    'Sudhan Sanjay VP', 'Sanjai M', 'V S Sachu', 'Dinesh J', 'Manickam S',
    'Pavithran S', 'Bharath N', 'Harihara Sudhan J P', 'Harivignesh S',
    'Elavazhagan D', 'Sanjay R', 'Deena S', 'S Sanjay', 'Rithik CA', 'Deepak P',
    'Sricharan I', 'Riduvarsshini R P', 'Dharaneesh B', 'Santhosh G', 'Ilamathi D',
    'A Madhan Arasu', 'Kamalesh A', 'Nithishbala P', 'A Yohesh', 'Kalai Selvan K',
    'Lalithkumar M', 'Manoj Kannan G', 'E Joysamuvel', 'Arthanari S', 'Akash Kanna S',
    'Nirmalraj K', 'Rohit K C', 'Sneghadhara Kumar', 'Sanjay N', 'Praveen D',
    'Arunaesh Kanna A K', 'Mathumithra T', 'Abinaya G', 'Dhanushree', 'Santhiya A K',
    'C P Sruthi', 'Akarshana S', 'Shadhanan S', 'Dhanush P', 'Gopinath V',
    'Harini Sri S', 'Milind Krishna', 'Dhanika D', 'Srinath G', 'Srisanth M',
    'R E Vikas', 'P K Yeshwini', 'S Sudharsan', 'Pavithralakshmi P', 'Dhinesh D',
    'Pavithran D', 'Athulya A M', 'NavaGeevithan G', 'Aishvarya S', 'Gowtham S',
    'Nandha R', 'Kishore', 'Arunn D', 'Asokan D', 'Neena Murali', 'Manigandan MS',
    'Sivaraj S', 'Neena Murali', 'Arjun Dev V A', 'Kamaleswaran S N', 'Deepa S',
    'Ridhun Varunith M R', 'Boopathipandiyan', 'Aakash S S', 'Mohammed Riyas A',
    'Mohammed Ashfaq', 'Abdul Razzaq B', 'Kavya Sree A', 'Nishanth S', 'Ajay R',
    'T Rithesh Kumar', 'Jesli Prince D', 'Krishnan S', 'Thrisanth M', 'Jayapriya A',
    'Kanishka', 'Naveen Kumar C', 'Sabarees S', 'M Vignesh', 'Divya Dharaneesh R S',
    'Sreya P', 'K Sathishkumar', 'Vikas D S', 'Krishnakumar', 'Mohan Raja V',
    'Priyadharshini S', 'Nagappan SP', 'Midhun DG', 'Kannan N', 'Saranyasree R',
    'Azhakesh G', 'Kapeesh N B', 'Kelwin Aanies V', 'Ghovarthan S', 'Mahashree A M',
    'Gowtham K', 'Nandhakumar E', 'Kishore S', 'S Nithish Kumar', 'Saran G',
    'R Ilamaran', 'Malini M', 'Pragatheesh S', 'Arun S R', 'Aryah SK',
    'Dhineshkalimuthu S', 'Dhanushree N', 'Gopi Chand S', 'Srinivasan B',
    'Dheenananth D', 'D Divya', 'Dhayanithi M', 'Chandru S', 'Dharanishwaran A',
    'S Ananth', 'Akhil P', 'A S Anbarasu', 'Anithan I', 'Balavanchi B',
    'Koushika Shree R', 'D Sugandha Kumar', 'Pradeep', 'Ragavendran', 'Vasanth P',
    'Ajay Madhav S', 'Godson A', 'K S Rosenpranav', 'M Vishwa', 'M Navinkumar',
    'Harish M', 'Sribalaji P', 'Dharanesh S', 'Aswiga U', 'Rohith G S',
    'P Arulkumaran', 'Sivaranjith S', 'Muthulakshmi G', 'Pradeep P',
    'Vijaya Bashkaran K', 'Raguraman S', 'Jones Geneva D', 'Kevin Maria Arockiya X',
    'Abel Jesuswin K', 'Rengasamy T', 'Sakthi M', 'Muthukaruppasmay N', 'Madesh S',
    'Aishwarya V', 'Nithin K S', 'Sudharsun V', 'Gowtham G', 'Gokul Sri M',
    'Gobika R', 'Barath P', 'Rahul', 'Anirudhan C', 'Dharshini T',
    'S Dhivya Dharishini', 'Nandhini', 'Bharath Manikandan K', 'Harishbabu M',
    'Dharshini Priya S', 'Avanthiga E', 'Naneshwaran M', 'Rajesh G',
    'Kaavyatamizhan K', 'Abishek R L', 'Nikhitha Selvaraj', 'Sanjay M',
    'Roshan Anto J', 'Pradhap S', 'G Anushree', 'Sai Mrithul Premanand',
    'Manendhiran K', 'S Mathanprasath', 'Ruthran K', 'Kishore Vedhupillai J A',
    'Kamaladharshini R', 'Nekasri B', 'N Mohamed Yaseen', 'Rohini S', 'Ramya M',
    'Patteeswaran S', 'Gowtham V', 'Rupesh Kumaran K R', 'Kaviya A', 'Prakash M',
    'Francis Linus A', 'Hari Prasath A', 'Poornima M', 'Saliny Devy S',
    'K Ramya Krishna', 'Mohanaprasath S', 'Ajay Kumar M', 'Premraj R', 'Nikhil R',
    'Mitun S', 'C D Shree Kaniish', 'Vishnu R', 'Narran S', 'Ragul D', 'Aarthi V G',
    'M Sandhiya', 'Vishali S', 'A Akshaya', 'A S Vishaal', 'Kamalesh J', 'Kanitha K',
    'Vishwa K', 'Narasimman S', 'Suresh D', 'Wincy Veronika J', 'Vishal L',
    'Monishsundar R', 'Sai Prasanth J M', 'Thanujasibaani US', 'Saravanakumar A',
    'Vaishnavi R', 'Guruprasath S', 'Yogish S', 'Thirumalai R', 'Nithish U',
    'V Vetriselvan', 'Poovarasan S', 'M Sanjeevi Kumar', 'Vasanth T N',
    'Sasmita R N', 'Sri Harini S', 'Saujanya VL', 'Harini R', 'Swetha M',
    'S M B Mahaboob Mariam', 'D Thavasi Perumal', 'Vinaya R', 'Sujith S',
    'Sakthivishal', 'Neha Sri R', 'Sanjaysv', 'Sakeswaran I', 'Karuppusamy T',
    'Akash S', 'Harishankar Iyer', 'Maria Selciya M', 'Lakshanika M S B',
    'M Gobika', 'Yaswanth M', 'Sri Hari N', 'Jeyasri J', 'Kishore S', 'Ragavi K',
    'Harish R', 'Dineshkumar S', 'KanagaDurga D', 'Sudharsan R', 'Kanagapriya D',
    'Nithin Aadhitya M N', 'Preethi K', 'Sakthi Priyaa', 'Cheralaathan R',
    'K Jayabharathi', 'S Hamdha', 'Bibin Sanju S', 'Rashwanth N M', 'Muktha Yuki R',
    'Naveen S', 'Narthana Sri R J', 'Karthik Kumar M', 'Dhanushree S', 'Syed Aadhil',
    'Hariharan R', 'Meleesa A C', 'Indhu Harini R', 'Anbuselvan SM',
    'Athul M Praveen', 'Sruthi V', 'Mahalakshmi S', 'Dakshata R',
    'Divya Dharshini CG', 'J Seyyad Alima Afrin', 'Saranya M', 'S Sanjay',
    'J Jinisha', 'Mathan M', 'Suryaprakashan A', 'Aravind Raj J', 'Boomika P',
    'S Sridhar', 'Dharshini M', 'Aisha Amna A', 'Dhakshida', 'Mugillendhan S',
    'Iliyas J', 'Mehavarsha S', 'R Mahizhavarthini', 'Srimathi S',
    'N Reema Khanam', 'Darshan S', 'Thangeshwari J', 'Atchaya A', 'Mownish C',
    'Abinaya M', 'Vimal Jothi V', 'Heavenly J', 'Varsha VR', 'Vasanth Hariharan S',
    'Shrivathsan V', 'Priyadharshini A', 'Janaki Raman E', 'Giripriyan S',
    'Anugraha S', 'Sanjeykrishna V', 'Ashwin S', 'Killivalavan T', 'Pugazhendhi S',
    'Kamalesh VK', 'Sudhan S', 'M I Mohammed Aaqil', 'Viruksha A S', 'Venkatesh V',
    'Mohamed Dharik S', 'Aneesh Fathima A R', 'Elakiya J', 'Madhumitha V',
    'Kanimozhi B', 'B Sandeepbharathi', 'Dhanasekar A', 'Srini', 'Sasidaran',
    'Sivakumaran M', 'Pravee SP', 'Arungiri T', 'Vikashini K', 'Vinodha M',
    'Joshua Matrix I', 'Jaihindh V', 'Sandhiya K', 'Theerthana K S',
    'Logavarsshini A', 'Vignesh S', 'Kanchana S', 'Kumaran S', 'Guru Prasath S',
    'Mirnalini G', 'Yashika Sri E', 'B Sasmila', 'Keerthieswari P', 'Hariharan M',
    'Vimal R', 'Sujan S', 'Pranavan K R', 'Sathya G', 'Geo Jeevan Raj C',
    'P Arulkumaran', 'Kabil Kumar B', 'Guruprasanth S', 'Abdul Shahadh R A',
    'Charan M', 'S Shanmathi', 'P Sriponsibi', 'Ranil Nideesh R', 'D Thirshanth',
    'Vishnu Subaiyan M', 'Princy Maria R', 'Ajay N', 'Karthi P', 'Athulya',
    'Jeyasakthi R', 'Guru Prasad S', 'Kayathri R D', 'Vishnu B', 'Adarsh A G',
    'Sandhiya S', 'Hariprasaath R', 'K S Revanth', 'Sangeerthan S', 'Dharanidharan',
    'Pooja P'
]

# Directory containing student photos
student_dir = os.path.join(os.getcwd(), 'photouploads', 'Students')

def extract_name_from_filename(filename):
    """Extract the actual name from filename patterns like '714020104002_ABIRAMI P - Abirami. P'"""
    base_name = os.path.splitext(filename)[0]
    
    # Pattern 1: "number_name - actual_name" format
    if ' - ' in base_name:
        parts = base_name.split(' - ')
        if len(parts) >= 2:
            return parts[1].strip()
    
    # Pattern 2: "number_name" format (extract after underscore)
    if '_' in base_name:
        parts = base_name.split('_')
        if len(parts) >= 2:
            return parts[1].strip()
    
    # If no pattern matches, return the base name
    return base_name

def normalize_name(name):
    """Normalize name by removing dots from initials and cleaning up"""
    # Remove dots from initials (like "A. P" -> "A P")
    name = re.sub(r'\.\s*', ' ', name)
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name)
    # Convert to lowercase for comparison
    return name.strip().lower()

# Build a mapping from normalized extracted names to actual filenames
file_map = {}
for filename in os.listdir(student_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        extracted_name = extract_name_from_filename(filename)
        normalized_name = normalize_name(extracted_name)
        file_map[normalized_name] = filename
        print(f"Extracted: '{extracted_name}' -> '{normalized_name}' from '{filename}'")

print(f"\nFound {len(file_map)} files to process")

# Rename files to match the target names
renamed_count = 0
for target in student_names:
    norm_target = normalize_name(target)
    if norm_target in file_map:
        old_name = file_map[norm_target]
        ext = os.path.splitext(old_name)[1]
        new_name = f"{target}{ext if ext else '.png'}"
        old_path = os.path.join(student_dir, old_name)
        new_path = os.path.join(student_dir, new_name)
        
        if old_path != new_path:
            if os.path.exists(new_path):
                print(f"Warning: {new_name} already exists, skipping {old_name}")
                continue
            os.rename(old_path, new_path)
            print(f"Renamed: {old_name} -> {new_name}")
            renamed_count += 1
        else:
            print(f"File {old_name} already has correct name")
    else:
        print(f"No match found for: {target}")

print(f"\nRenaming process completed! Files renamed: {renamed_count}") 