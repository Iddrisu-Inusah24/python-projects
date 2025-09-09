-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 26, 2025 at 04:20 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `attendance_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `status` varchar(10) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`id`, `student_id`, `status`, `date`, `created_at`) VALUES
(346, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(347, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(348, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(349, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(350, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(351, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(352, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(353, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(355, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(356, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(357, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(358, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(359, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(360, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(361, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(362, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(363, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(364, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(365, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(366, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(367, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(368, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(369, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(370, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(371, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(372, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(373, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(374, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(375, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(376, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(377, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(378, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(379, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(380, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(381, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(382, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(383, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(386, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(387, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(388, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(389, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(390, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(391, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(392, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(393, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(394, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(395, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(396, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(397, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(398, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(399, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(400, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(401, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(402, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(403, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(404, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(405, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(406, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(407, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(408, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(409, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(410, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(411, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(412, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(413, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(414, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(415, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(416, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(417, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(418, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(419, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(420, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(421, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(422, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(423, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(424, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(425, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(426, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(427, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(428, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(429, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(430, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(431, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(432, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(433, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(434, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(435, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(436, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(437, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(438, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(439, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(440, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(441, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(442, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(443, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(444, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(445, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(446, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(447, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(448, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(449, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(450, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(451, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(452, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(453, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(454, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(455, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(456, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(457, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(458, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(459, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(460, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(461, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(462, 38, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(463, 40, 'Absent', '2025-08-26', '2025-08-26 13:56:34'),
(464, 39, 'Present', '2025-08-26', '2025-08-26 13:56:34'),
(465, 41, 'Absent', '2025-08-26', '2025-08-26 13:56:34'),
(466, 43, 'Absent', '2025-08-26', '2025-08-26 13:56:34'),
(467, 42, 'Absent', '2025-08-26', '2025-08-26 13:56:34');

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `id` int(11) NOT NULL,
  `label` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sessions`
--

INSERT INTO `sessions` (`id`, `label`, `created_at`) VALUES
(1, 'Backup 1', '2025-08-25 15:21:52'),
(2, 'Session 2', '2025-08-25 15:22:16'),
(3, 'Session 3', '2025-08-26 12:22:45');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `status` varchar(20) DEFAULT 'Present'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `first_name`, `last_name`, `status`) VALUES
(38, 'Iddrisu', 'Adelga', 'Present'),
(39, 'Adam', 'Smith', 'Present'),
(40, 'Aba', 'Jhds', 'Present'),
(41, 'Hjhsd', 'Lkds', 'Present'),
(42, 'Nkjcx', 'Jkjcx', 'Present'),
(43, 'Kjolcx', 'Kjjlkxcz', 'Present');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_name` (`first_name`,`last_name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=468;

--
-- AUTO_INCREMENT for table `sessions`
--
ALTER TABLE `sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
