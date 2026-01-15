from datetime import datetime
import os


def process_entry(object, format_data):

    return {
        "name": object.name,
        "size_kb": object.stat().st_size / 1024,
        "modification": format_data[1],
        "creation": format_data[0],
        "path": object.path,
        "type": "directory" if object.is_dir() else "file",
    }


try:

    def hever(Path, typeSearch="all", Pattern=None, depth=0):
        have_patterns = set(Pattern) if Pattern else set()
        try:
            with os.scandir(Path) as it:
                for entries in it:
                    try:

                        if depth > 0 and entries.is_dir():
                            # aqui o valor depth esta sendo subtraido -1
                            yield from hever(
                                entries.path, typeSearch, Pattern, depth - 1
                            )

                        if typeSearch in ("file", "files") and not entries.is_file():
                            continue
                        # Se quero pastas e não é uma pasta => ignora
                        if typeSearch in ("dir", "dirs") and not entries.is_dir():
                            continue

                        if have_patterns and not any(
                            x.lower() in entries.name.lower() for x in have_patterns
                        ):
                            continue

                        stat = entries.stat()

                        ts_change = getattr(stat, "st_birthtime", stat.st_ctime)
                        ctime = datetime.fromtimestamp(ts_change).strftime("%d/%m/%Y")
                        mtime = datetime.fromtimestamp(stat.st_mtime).strftime(
                            "%d/%m/%Y"
                        )

                        yield process_entry(entries, (ctime, mtime))

                    except OSError as err:
                        print(f"{err} in {entries.name}")

        except (FileNotFoundError, PermissionError) as F:
            print(f"{F}")
            return  # Se o arquivo sumiu entre a listagem e a leitura # Se não tiver permissão, apenas ignora

except (ValueError, ModuleNotFoundError) as error:
    print(f"{error}")
except:
    print(ValueError)




# funcao = searchy("C:/",Pattern={'program'},depth=0)
# print(type(searchy("C:/")))
# for i in funcao:
#     print(i['name'])
