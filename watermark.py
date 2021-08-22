import cv2


def multiple_images(image, shape):
    """
    изменяет размеры картинкы и повторяет туже картинку.
    используется только для картинок с gipernn.ru
    :param image: картинка которая должна быть изменена
    :param shape: размеры итоговой картинкы
    :return: итоговая картинка
    """
    count_rows = shape[0] // image.shape[0] - 1
    count_columns = shape[1] // image.shape[1] - 1
    output_image = image
    for _ in range(count_rows):
        output_image = cv2.vconcat([output_image, image])

    output_image = cv2.vconcat([output_image, image[:(shape[0] - output_image.shape[0]), :, :]])

    image = output_image

    for _ in range(count_columns):
        output_image = cv2.hconcat([output_image, image])

    output_image = cv2.hconcat([output_image, image[:, :(shape[1] - output_image.shape[1]), :]])

    return output_image


def set_watermark(background_image, source_website, big_logo_path, small_logo_path):
    """
    подстовляет логотип зависив от сайта с которой взят бэкграунд
    :param background_image: картинка на которой должен ставиться логотип
    :param source_website: имя сайта источника
    (avito.ru, cian.ru, irr.ru, youla.io, sob.ru, bazarpnz.ru, kupiprodai.ru,
    move.ru, realty.yandex.ru, moyareklama.ru, dom.sakh.com, gipernn.ru, mlsn.ru, orsk.ru)
    :param big_logo_path: ссылка на картинку болшого логотипа
    :param small_logo_path: ссылка на картинку маленького логотипа
    :return: картинка с новым логотипом
    """
    overlay_image = None
    alpha = 0.0
    beta = 0.0
    if source_website == "avito.ru":
        logo = cv2.imread(big_logo_path)
        logo = cv2.resize(logo, (background_image.shape[1], min(int(background_image.shape[1] * 1.2),
                                                                background_image.shape[0])))
        overlay_image = cv2.copyMakeBorder(logo,
                                           (background_image.shape[0] - logo.shape[0]) // 2,
                                           background_image.shape[0] - ((background_image.shape[0] +
                                                                         logo.shape[0]) // 2),
                                           (background_image.shape[1] - logo.shape[1]) // 2,
                                           background_image.shape[1] - ((background_image.shape[1] +
                                                                         logo.shape[1]) // 2),
                                           cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 1.0
        beta = 0.75

    elif source_website == 'cian.ru':
        logo = cv2.imread(big_logo_path)
        logo = cv2.resize(logo, (background_image.shape[1] // 2, background_image.shape[0] // 2))
        overlay_image = cv2.copyMakeBorder(logo[:-(background_image.shape[0] // 10), :, :],
                                           background_image.shape[0] - logo.shape[0] + (
                                                   background_image.shape[0] // 10),
                                           0,
                                           background_image.shape[1] - logo.shape[1],
                                           0,
                                           cv2.BORDER_CONSTANT, (0, 0, 0))
        alpha = 1.0
        beta = 0.9

    elif source_website == "irr.ru" or source_website == "kupiprodai.ru":
        logo = cv2.imread(small_logo_path)
        logo = cv2.resize(logo, (min(341, background_image.shape[1]), min(227, background_image.shape[0])))
        overlay_image = cv2.copyMakeBorder(
            logo[:-(logo.shape[0] // 4), :-(3 * logo.shape[1] // 30), :],
            background_image.shape[0] - logo.shape[0] + (logo.shape[0] // 4),
            0,
            background_image.shape[1] - logo.shape[1] + (3 * logo.shape[1] // 30),
            0,
            cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 0.9
        beta = 2.0

    elif source_website == "youla.io" or source_website == "sob.ru" or source_website == "mlsn.ru":
        logo = cv2.imread(big_logo_path)
        logo = cv2.resize(logo, (min(300, background_image.shape[1]), min(200, background_image.shape[0])))
        overlay_image = cv2.copyMakeBorder(logo[:, :, :],
                                           background_image.shape[0] - logo.shape[0],
                                           0,
                                           background_image.shape[1] - logo.shape[1],
                                           0,
                                           cv2.BORDER_CONSTANT, (0, 0, 0))
        alpha = 1.0
        beta = 0.7

    elif source_website == "bazarpnz.ru":
        logo = cv2.imread(small_logo_path)
        logo = cv2.resize(logo[:, 50:, :], (450, 266))
        overlay_image = cv2.copyMakeBorder(logo,
                                           (background_image.shape[0] - logo.shape[0]) // 2,
                                           background_image.shape[0] - ((background_image.shape[0] +
                                                                         logo.shape[0]) // 2),
                                           (background_image.shape[1] - logo.shape[1]) // 2,
                                           background_image.shape[1] - ((background_image.shape[1] +
                                                                         logo.shape[1]) // 2),
                                           cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 1.0
        beta = 1.2

    elif source_website == "move.ru":
        logo = cv2.imread(big_logo_path)
        logo = cv2.resize(logo, (min(background_image.shape[1], 225), min(background_image.shape[0], 200)))
        overlay_image = cv2.copyMakeBorder(
            logo[:-(3 * logo.shape[0] // 10), :-(logo.shape[1] // 15), :],
            background_image.shape[0] - logo.shape[0] + (3 * logo.shape[0] // 10),
            0,
            background_image.shape[1] - logo.shape[1] + (logo.shape[1] // 15),
            0,
            cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 0.9
        beta = 2.0

    elif source_website == "realty.yandex.ru":
        logo = cv2.imread(small_logo_path)
        logo = cv2.resize(logo, (min(background_image.shape[1], 300), min(background_image.shape[0], 192)))
        print(background_image.shape)
        overlay_image = cv2.copyMakeBorder(
            logo[(logo.shape[0] // 3):, (logo.shape[1] // 6):, :],
            0,
            background_image.shape[0] - logo.shape[0] + (logo.shape[0] // 3),
            0,
            background_image.shape[1] - logo.shape[1] + (logo.shape[1] // 6),
            cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 1.0
        beta = 2.0

    elif source_website == "moyareklama.ru":
        logo = cv2.imread(big_logo_path)
        logo = cv2.resize(logo, (min(background_image.shape[1], 231), min(background_image.shape[0], 280)))
        overlay_image = cv2.copyMakeBorder(logo[:-(logo.shape[0] // 13), :, :],
                                           (background_image.shape[0] - logo.shape[0]) // 2 + logo.shape[0] // 13,
                                           background_image.shape[0] - ((background_image.shape[0] +
                                                                         logo.shape[0]) // 2),
                                           (background_image.shape[1] - logo.shape[1]) // 2,
                                           background_image.shape[1] - ((background_image.shape[1] +
                                                                         logo.shape[1]) // 2),
                                           cv2.BORDER_CONSTANT, (0, 0, 0))
        alpha = 1.0
        beta = 1.0

    elif source_website == "dom.sakh.com":
        logo = cv2.imread(big_logo_path)
        logo = cv2.resize(logo, (min(background_image.shape[1], int(background_image.shape[0])),
                                 background_image.shape[0] // 2))
        overlay_image = cv2.copyMakeBorder(logo,
                                           6 * (background_image.shape[0] - logo.shape[0]) // 7,
                                           background_image.shape[0] - logo.shape[0] - 6 *
                                           (background_image.shape[0] - logo.shape[0]) // 7,
                                           (background_image.shape[1] - logo.shape[1]) // 2,
                                           background_image.shape[1] - ((background_image.shape[1] +
                                                                         logo.shape[1]) // 2),
                                           cv2.BORDER_CONSTANT, (0, 0, 0))
        alpha = 1.0
        beta = 1.2

    elif source_website == "gipernn.ru":
        logo = cv2.imread(big_logo_path)
        logo = cv2.resize(logo, (200, 350))
        logo = cv2.copyMakeBorder(logo, 0, 0, 70, 0, cv2.BORDER_CONSTANT, (0, 0, 0))
        logo = logo[58:-100, 30:-20, :]
        overlay_image = multiple_images(logo, background_image.shape)

        alpha = 1.0
        beta = 1.5

    elif source_website == "orsk.ru":
        logo = cv2.imread(big_logo_path)
        logo = cv2.resize(logo, (min(background_image.shape[1], 355), background_image.shape[0] // 2))
        overlay_image = cv2.copyMakeBorder(logo,
                                           (background_image.shape[0] - logo.shape[0]) // 2,
                                           background_image.shape[0] - ((background_image.shape[0] +
                                                                         logo.shape[0]) // 2),
                                           (background_image.shape[1] - logo.shape[1]) // 2,
                                           background_image.shape[1] - ((background_image.shape[1] +
                                                                         logo.shape[1]) // 2),
                                           cv2.BORDER_CONSTANT, (0, 0, 0))
        alpha = 1.0
        beta = 0.8

    result = cv2.addWeighted(background_image, alpha, overlay_image, beta, 0)
    return result
