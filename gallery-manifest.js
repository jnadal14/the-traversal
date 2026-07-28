/**
 * Gallery order — edit this file only. Use URL-safe filenames (kebab-case, no & or <).
 *
 * Width and height reserve each tile before its media loads, preventing the masonry
 * from shifting while visitors scroll. Run ./scripts/optimize-gallery-images.sh after
 * adding large scans.
 */
window.GALLERY_MANIFEST = (() => {
    const image = (src, width, height, alt) => ({ type: 'image', src, width, height, alt });
    const video = (src) => ({
        type: 'video',
        src: `${src}?v=20260728`,
        poster: src
            .replace(/^CLIPS\//, 'IMAGES/video-posters/')
            .replace(/\.mp4$/i, '.jpg'),
        width: 16,
        height: 9,
    });

    return [
        image('IMAGES/01.jpg', 2000, 2500),
        image('IMAGES/new/ellipsis-heart.jpg', 2200, 1467),
        image('IMAGES/03.jpg', 2000, 1325),
        video('CLIPS/02_SAS_1.mp4'),
        image('IMAGES/02.jpg', 2000, 1124),
        image('IMAGES/new/ellipsis-light.jpg', 1760, 2200),
        video('CLIPS/01_AWAGA_1.mp4'),
        image('IMAGES/new/man-under-snowy-mountain.jpg', 2200, 1458),
        image('IMAGES/04.jpg', 2000, 1325),
        image('IMAGES/05.jpg', 1760, 2200),
        image('IMAGES/06.jpg', 2000, 1325),
        image('IMAGES/new/ellipsis-room.jpg', 2200, 1458),
        image('IMAGES/07.jpg', 2000, 1325),
        image('IMAGES/08.jpg', 1760, 2200),
        image('IMAGES/10.jpg', 2000, 1124),
        image('IMAGES/new/cass-and-aiden.jpg', 2200, 1458),
        image('IMAGES/new/bar-tartare.jpg', 2200, 1458),
        image('IMAGES/new/ellipsis-corner.jpg', 1458, 2200),
        image('IMAGES/new/neon-cola.jpg', 2200, 1459),
        image('IMAGES/new/ellipsis-room.jpg', 2200, 1458),
        video('CLIPS/03_Fire_lookout_1.mp4'),
        image('IMAGES/11.jpg', 2000, 1325),
        image('IMAGES/12.jpg', 2000, 1325),
        image('IMAGES/13.jpg', 2000, 1325),
        video('CLIPS/04_abott_2.mp4'),
        image('IMAGES/14.jpg', 2000, 1325),
        image('IMAGES/15.jpg', 1760, 2200),
        video('CLIPS/05_Icefileds_1.mp4'),
        image('IMAGES/16.jpg', 2000, 1325),
        image('IMAGES/18.jpg', 1760, 2200),
        image('IMAGES/19.jpg', 2000, 1325),
        video('CLIPS/06_abott_1.mp4'),
        image('IMAGES/21.jpg', 1760, 2200),
        image('IMAGES/22.jpg', 2000, 1325),
        image('IMAGES/new/ethan-and-roman.jpg', 2200, 1458),
        image('IMAGES/23.jpg', 1760, 2200),
        image('IMAGES/24.jpg', 2000, 1325),
        image('IMAGES/25.jpg', 2000, 1325),
        image('IMAGES/26.jpg', 2000, 1325),
        video('CLIPS/07_Fire_lookout_2.mp4'),
        image('IMAGES/27.jpg', 1760, 2200),
        image('IMAGES/28.jpg', 2000, 1325),
        video('CLIPS/08_Icefileds_2.mp4'),
        image('IMAGES/29.jpg', 2000, 1325),
        image('IMAGES/30.jpg', 2000, 1325),
        image('IMAGES/31.jpg', 1760, 2200),
        video('CLIPS/09_SAS_2.mp4'),
        image('IMAGES/32.jpg', 1760, 2200),
        image('IMAGES/33.jpg', 1760, 2200),
    ];
})();
