-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 15, 2024 at 01:11 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `career_recommend`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `cr_category`
--

CREATE TABLE `cr_category` (
  `id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cr_category`
--

INSERT INTO `cr_category` (`id`, `category`) VALUES
(1, 'Engineering'),
(2, 'Arts'),
(3, 'Economics');

-- --------------------------------------------------------

--
-- Table structure for table `cr_college`
--

CREATE TABLE `cr_college` (
  `id` int(11) NOT NULL,
  `college_type` varchar(20) NOT NULL,
  `college` varchar(100) NOT NULL,
  `location` varchar(40) NOT NULL,
  `district` varchar(30) NOT NULL,
  `cat` varchar(30) NOT NULL,
  `course` varchar(20) NOT NULL,
  `detail` varchar(30) NOT NULL,
  `percent` double NOT NULL,
  `sem_fees` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cr_college`
--

INSERT INTO `cr_college` (`id`, `college_type`, `college`, `location`, `district`, `cat`, `course`, `detail`, `percent`, `sem_fees`) VALUES
(1, 'Government', 'Arignar Anna Govt. Arts College', 'Billanakuppam', 'Krishnagiri', 'Arts', 'BSc', 'Computer Science', 60, 4000),
(2, 'Private', 'St.Josephs College Of Engineering', 'Sholinganallur', 'Chennai', 'Engineering', 'BE', 'Computer Science', 75, 25000),
(3, 'Private', 'CK College of Engineering & Technology', 'Jayaram Nagar, Chellangkuppam', 'Cuddalore', 'Engineering', 'BE', 'Computer Science', 70, 20000),
(4, 'Government', 'Government College of Engineering', 'Madepalli', ' Bargur', 'Engineering', 'BE', 'Computer Science', 85, 8000),
(5, 'Government', 'Government College of Engineering', 'Madepalli', ' Bargur', 'Engineering', 'B.Tech', 'Information Technology', 85, 8000),
(6, 'Private', 'St.Josephs College Of Engineering', 'Sholinganallur', 'Chennai', 'Engineering', 'B.Tech', 'Information Technology', 75, 22000),
(7, 'Government', 'Government Arts College', 'Maravaneri', 'Salem', 'Economics', 'B.Com', 'Commerce', 70, 3000),
(8, 'Private', 'Vysya College', 'Masinaickenpatti', 'Salem', 'Economics', 'B.Com', 'Commerce', 75, 4000),
(9, 'Private', 'Parisutham Institute of Technology and Science', 'Nanjikottai', 'Thanjavur', 'Economics', 'B.Com', 'Commerce', 75, 4500),
(10, 'Government', 'Rajah serfoji Government Arts College', 'AVP Azhagammal Nagar', 'Thanjavur', 'Economics', 'BBA', 'Business Administration', 75, 3500),
(11, 'Private', 'Valluvar College of Science and Management', 'Puthambur', 'Valluvar College of Science an', 'Economics', 'BBA', 'Business Administration', 70, 3000);

-- --------------------------------------------------------

--
-- Table structure for table `cr_course`
--

CREATE TABLE `cr_course` (
  `id` int(11) NOT NULL,
  `catid` int(11) NOT NULL,
  `course` varchar(20) NOT NULL,
  `detail` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cr_course`
--

INSERT INTO `cr_course` (`id`, `catid`, `course`, `detail`) VALUES
(1, 1, 'BE', 'Computer Science'),
(2, 1, 'B.Tech', 'Information Technology'),
(3, 2, 'BSc', 'Computer Science'),
(4, 2, 'BCA', 'Computer Application'),
(5, 3, 'B.Com', 'Commerce'),
(6, 3, 'BBA', 'Business Administration');

-- --------------------------------------------------------

--
-- Table structure for table `cr_question`
--

CREATE TABLE `cr_question` (
  `id` int(11) NOT NULL,
  `question` varchar(200) NOT NULL,
  `option1` varchar(100) NOT NULL,
  `option2` varchar(100) NOT NULL,
  `option3` varchar(100) NOT NULL,
  `option4` varchar(100) NOT NULL,
  `answer` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cr_question`
--

INSERT INTO `cr_question` (`id`, `question`, `option1`, `option2`, `option3`, `option4`, `answer`) VALUES
(1, 'What are your interests primarily focused on?', 'Science and Technology', 'Art and Design', 'Business and Management', 'Humanities and Social Sciences', '2'),
(2, 'What type of work environment do you prefer?', 'Laboratory or Research Setting', 'Creative Studio or Workshop', 'Corporate Office or Business Environment', 'Classroom or Community Setting', '2'),
(3, 'Which of the following skills do you possess or would like to develop further?', 'Problem-solving and analytical skills', 'Creativity and artistic skills', 'Leadership and management skills', 'Communication and interpersonal skills', '2'),
(4, 'What motivates you the most in a potential career?', 'Making scientific discoveries or technological advancements', 'Expressing creativity and imagination', 'Building successful businesses or managing projects', 'Making a positive impact on society or individuals', '2'),
(5, 'What type of tasks do you enjoy doing the most?', 'Conducting experiments or analyzing data', 'Creating artwork or designing projects', 'Planning strategies or managing finances', 'Interacting with people or helping others', '2'),
(6, 'Which subject did you excel in or enjoy the most during your high school studies?', 'Mathematics or Physics', 'Art or Design', 'Economics or Business Studies', 'History or Literature', '2'),
(7, 'What are your long-term career goals?', 'Pursuing a career in research or academia', 'Becoming a professional artist or designer', 'Starting your own business or managing a company', 'Working in public service or social advocacy', '2'),
(8, 'Which industry or field are you most passionate about?', 'Healthcare and Medicine', 'Media and Entertainment', 'Finance and Banking', 'Education and Non-profit Sector', '2'),
(9, 'What level of education are you willing to pursue?', 'Bachelor Degree', 'Master Degree', 'Professional Certification', 'Vocational Training', '2'),
(10, 'Where do you see yourself in the next five to ten years?', 'Advancing in a specialized career field', 'Establishing your own business or brand', 'Climbing the corporate ladder in a managerial role', 'Contributing to society through public service or activism', '2'),
(11, 'How important is the availability of specialized facilities or resources related to your chosen field of study?', 'Not important', 'Important', 'Somewhat important', 'Very important', '2'),
(12, 'How you choosen that field by?', 'Interest', 'Parents pressure', 'Teachers advice', 'Degree worth', '1'),
(13, 'What are your current studying results?', 'Excellent', 'Good', 'Satisfactory', 'Fair & no', '4'),
(14, 'College Preferred for?', 'Any', 'University', 'Government', 'Private', '3'),
(15, 'College preferred location?', 'Any', 'Native City', 'Other District', 'Other State', '3');

-- --------------------------------------------------------

--
-- Table structure for table `cr_recommend`
--

CREATE TABLE `cr_recommend` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `answer1` varchar(50) NOT NULL,
  `answer2` varchar(50) NOT NULL,
  `answer3` varchar(50) NOT NULL,
  `answer4` varchar(50) NOT NULL,
  `answer5` varchar(50) NOT NULL,
  `answer6` varchar(50) NOT NULL,
  `answer7` varchar(50) NOT NULL,
  `answer8` varchar(50) NOT NULL,
  `answer9` varchar(50) NOT NULL,
  `answer10` varchar(50) NOT NULL,
  `answer11` varchar(50) NOT NULL,
  `answer12` varchar(50) NOT NULL,
  `answer13` varchar(50) NOT NULL,
  `answer14` varchar(50) NOT NULL,
  `answer15` varchar(50) NOT NULL,
  `answer16` varchar(50) NOT NULL,
  `answer17` varchar(50) NOT NULL,
  `answer18` varchar(50) NOT NULL,
  `answer19` varchar(50) NOT NULL,
  `answer20` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cr_recommend`
--

INSERT INTO `cr_recommend` (`id`, `uname`, `answer1`, `answer2`, `answer3`, `answer4`, `answer5`, `answer6`, `answer7`, `answer8`, `answer9`, `answer10`, `answer11`, `answer12`, `answer13`, `answer14`, `answer15`, `answer16`, `answer17`, `answer18`, `answer19`, `answer20`) VALUES
(1, 'kumar', '', 'Certificates', 'no', 'Corporate Office or Business Environment', 'Problem-solving and analytical skills', 'Making scientific discoveries or technological adv', 'Conducting experiments or analyzing data', 'Mathematics or Physics', 'Pursuing a career in research or academia', 'Media and Entertainment', 'Bachelor Degree', 'Advancing in a specialized career field', 'Yes', 'Yes', 'Not important', 'Engineering', 'Degree worth', 'Good', 'Any', 'Chennai');

-- --------------------------------------------------------

--
-- Table structure for table `cr_recommend1`
--

CREATE TABLE `cr_recommend1` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `school_level` varchar(20) NOT NULL,
  `school_type` varchar(20) NOT NULL,
  `communication` varchar(20) NOT NULL,
  `subject` varchar(20) NOT NULL,
  `maths` double NOT NULL,
  `physics` double NOT NULL,
  `chemistry` double NOT NULL,
  `prizes` varchar(20) NOT NULL,
  `internship` varchar(20) NOT NULL,
  `courses` varchar(20) NOT NULL,
  `gap` varchar(20) NOT NULL,
  `scholarship` varchar(20) NOT NULL,
  `specialization` varchar(30) NOT NULL,
  `cgpa` double NOT NULL,
  `extra_curricular` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cr_recommend1`
--

INSERT INTO `cr_recommend1` (`id`, `uname`, `school_level`, `school_type`, `communication`, `subject`, `maths`, `physics`, `chemistry`, `prizes`, `internship`, `courses`, `gap`, `scholarship`, `specialization`, `cgpa`, `extra_curricular`) VALUES
(1, 'kumar', 'CBSE', 'Private', 'High', 'Maths', 95, 88, 83, 'No', '', '', '', '', '', 0, 'Yes');

-- --------------------------------------------------------

--
-- Table structure for table `cr_skills`
--

CREATE TABLE `cr_skills` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `stype` varchar(20) NOT NULL,
  `detail` varchar(100) NOT NULL,
  `filename` varchar(50) NOT NULL,
  `rdate` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cr_skills`
--

INSERT INTO `cr_skills` (`id`, `uname`, `stype`, `detail`, `filename`, `rdate`) VALUES
(1, 'kumar', 'Sports', 'Running, win 2nd price', 'S1ss1.jpg', '20-11-2023'),
(2, 'kumar', 'Skills', 'Drawing ', 'S2ss2.jpg', '20-11-2023');

-- --------------------------------------------------------

--
-- Table structure for table `cr_student`
--

CREATE TABLE `cr_student` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `dob` varchar(15) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `school1` varchar(50) NOT NULL,
  `mark1` double NOT NULL,
  `percent1` double NOT NULL,
  `school2` varchar(30) NOT NULL,
  `mark2` double NOT NULL,
  `percent2` double NOT NULL,
  `hs_group` varchar(100) NOT NULL,
  `sport` varchar(200) NOT NULL,
  `extra_cur` varchar(200) NOT NULL,
  `skill` varchar(200) NOT NULL,
  `level` varchar(20) NOT NULL,
  `college` varchar(50) NOT NULL,
  `ug_degree` varchar(20) NOT NULL,
  `ug_percent` double NOT NULL,
  `year` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cr_student`
--

INSERT INTO `cr_student` (`id`, `name`, `gender`, `dob`, `mobile`, `email`, `uname`, `pass`, `address`, `city`, `school1`, `mark1`, `percent1`, `school2`, `mark2`, `percent2`, `hs_group`, `sport`, `extra_cur`, `skill`, `level`, `college`, `ug_degree`, `ug_percent`, `year`) VALUES
(1, 'Kumar', 'Male', '2006-08-07', 9856428174, 'kumar@gmail.com', 'kumar', '123456', '45th, SG Nagar', 'Salem', 'BH School', 480, 96, 'AG School', 1150, 95.83, 'Physics/Chemistry/Statistics/Mathematics', 'Cricket,Tennis', 'Seminar Participated,Drawing,Music', 'Web Design', 'Engineering', 'SS College', 'BE', 84, '2020');
