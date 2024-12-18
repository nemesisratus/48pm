<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media Gallery</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f0f0f0;
        }

        .filter-container {
            margin-bottom: 20px;
        }

        select {
            padding: 8px;
            font-size: 16px;
            border-radius: 4px;
        }

        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }

        .media-item {
            background: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .media-item img {
            width: 100%;
            height: auto;
            border-radius: 4px;
        }

        .media-item audio {
            width: 100%;
            margin-top: 10px;
        }

        @media (max-width: 600px) {
            .gallery {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="filter-container">
        <select id="folderFilter">
            <option value="all">All members</option>
            <?php
            $baseDir = '/media/';
            $folders = array_filter(glob($baseDir . '*'), 'is_dir');
            foreach($folders as $folder) {
                $folderName = basename($folder);
                echo "<option value='$folderName'>$folderName</option>";
            }
            ?>
        </select>
    </div>

    <div id="gallery" class="gallery">
        <?php
        function getMediaFiles($dir) {
            $files = [];
            $files['images'] = glob($dir . '/*.{jpg,png}', GLOB_BRACE);
            $files['audio'] = glob($dir . '/*.mp3');
            return $files;
        }

        if(isset($_GET['folder'])) {
            $folder = $_GET['folder'];
            if($folder === 'all') {
                foreach($folders as $folder) {
                    $files = getMediaFiles($folder);
                    foreach($files['images'] as $image) {
                        echo "<div class='media-item'><img src='$image' alt='" . basename($image) . "'></div>";
                    }
                    foreach($files['audio'] as $audio) {
                        echo "<div class='media-item'><audio controls><source src='$audio' type='audio/mpeg'>Your browser does not support the audio element.</audio></div>";
                    }
                }
            } else {
                $dir = $baseDir . $folder;
                if(is_dir($dir)) {
                    $files = getMediaFiles($dir);
                    foreach($files['images'] as $image) {
                        echo "<div class='media-item'><img src='$image' alt='" . basename($image) . "'></div>";
                    }
                    foreach($files['audio'] as $audio) {
                        echo "<div class='media-item'><audio controls><source src='$audio' type='audio/mpeg'>Your browser does not support the audio element.</audio></div>";
                    }
                }
            }
        }
        ?>
    </div>

    <script>
        document.getElementById('folderFilter').addEventListener('change', function() {
            window.location.href = '?folder=' + this.value;
        });
    </script>
</body>
</html>
