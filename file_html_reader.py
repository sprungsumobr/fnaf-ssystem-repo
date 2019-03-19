# coding = utf-8
# using namespace std


class ArgumentNotExists(Exception):
    args = "This word not exists at all"
    pass


class SearchAll:

    def exists(self, file: str, ref_str: str):
        return ref_str in open(file, "r").read()


class SearchTags:

    def exists(self, file: str, tag_ref: str):
        if not "<" and ">" in tag_ref:
            tag_ref[0] = "<"
            tag_ref[-1] = ">"
        return tag_ref in open(file, "r").read()





































